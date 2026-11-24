from os import environ

from psycopg2 import errors

from odoo import _, fields, models
from odoo.exceptions import AccessError

from ..services.smartapi import CAPABILITIES, ProviderError, SmartAPI

_ADMIN = "golok_ai_trading_lab_pro.group_admin"
_AUTH_ENV = ("GOLOK_SMARTAPI_CLIENT_CODE", "GOLOK_SMARTAPI_PIN", "GOLOK_SMARTAPI_TOTP_CODE")


class ProviderBudget(models.Model):
    _name = "golok.lab.provider.budget"
    _description = "Read-only provider request budget"
    _log_access = False

    name = fields.Char(required=True)
    next_at = fields.Datetime(required=True)
    _identity = models.Constraint("UNIQUE(name)", "Provider budget already exists.")

    def _reserve_auth(self):
        # A failed call still consumes a slot in this database.
        try:
            with self.env.registry.cursor() as cursor:
                cursor.execute("SET LOCAL lock_timeout = '1s'")
                cursor.execute("""
                    INSERT INTO golok_lab_provider_budget (name, next_at)
                    VALUES ('smartapi_auth', (clock_timestamp() AT TIME ZONE 'UTC') + interval '60 seconds')
                    ON CONFLICT (name) DO UPDATE SET next_at = EXCLUDED.next_at
                    WHERE golok_lab_provider_budget.next_at <= (clock_timestamp() AT TIME ZONE 'UTC')
                    RETURNING id
                """)
                reserved = bool(cursor.fetchone())
                cursor.commit()
        except (errors.LockNotAvailable, errors.SerializationFailure):
            return False
        return reserved


class ProviderSetup(models.TransientModel):
    _name = "golok.lab.provider.setup"
    _description = "Read-only SmartAPI diagnostics"

    status = fields.Char(readonly=True, default="OFFLINE")
    details = fields.Text(readonly=True)
    checked_at = fields.Datetime(readonly=True)

    def _check_setup_rights(self):
        self.ensure_one()
        self.check_access("write")
        if not self.env.user.has_group(_ADMIN):
            raise AccessError(_("Only Trading System Administrators may diagnose the provider."))

    def _finish(self, status, details):
        self.write({"status": status, "details": details, "checked_at": fields.Datetime.now()})
        return {"type": "ir.actions.act_window", "res_model": self._name,
                "res_id": self.id, "views": [(False, "form")], "target": "new"}

    def _configuration(self):
        if environ.get("GOLOK_SMARTAPI_AUTHORIZED") != "1":
            return None, None, "OFFLINE", _("Real transport is disabled by local configuration.")
        try:
            client = SmartAPI.from_environment()
        except ProviderError:
            return None, None, "ERROR", _("Local provider settings are invalid.")
        credentials = tuple(environ.get(key) for key in _AUTH_ENV)
        if client.state == "NOT_CONFIGURED" or not all(credentials):
            return None, None, "NOT CONFIGURED", _("Configure the required provider variables on the Odoo host.")
        if any(len(value) > 128 for value in credentials):
            return None, None, "ERROR", _("Local authentication settings are invalid.")
        return client, credentials, "AUTHORIZATION REQUIRED", _(
            "Local configuration is present. Confirm entitlement, registered egress and a current TOTP before testing authentication."
        )

    def action_check_configuration(self):
        self._check_setup_rights()
        _, _, status, details = self._configuration()
        return self._finish(status, details + _(" Adapter capabilities: %s.", ", ".join(sorted(CAPABILITIES))))

    def action_test_authentication(self):
        self._check_setup_rights()
        client, credentials, status, details = self._configuration()
        if not client:
            return self._finish(status, details)
        if not self.env["golok.lab.provider.budget"]._reserve_auth():
            return self._finish("RATE LIMITED", _("Wait at least 60 seconds between attempts in this database."))
        try:
            client.authenticate(*credentials)
        except ProviderError:
            return self._finish(client.state, _("Authentication could not be verified. Check local settings and broker access."))
        return self._finish("AUTHENTICATED", _("One authentication call succeeded. The token was discarded and no market request was sent."))
