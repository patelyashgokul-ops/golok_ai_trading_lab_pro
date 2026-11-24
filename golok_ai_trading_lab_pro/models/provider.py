import hashlib
from datetime import datetime, timezone
from os import environ
from threading import Lock
from time import monotonic

from psycopg2 import errors

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..services import session_policy
from ..services.smartapi import CAPABILITIES, ProviderError, SmartAPI

_ADMIN = "golok_ai_trading_lab_pro.group_admin"
_AUTH_ENV = ("GOLOK_SMARTAPI_CLIENT_CODE", "GOLOK_SMARTAPI_PIN", "GOLOK_SMARTAPI_TOTP_CODE")
_IDENTITY_ENV = (_AUTH_ENV[0], "GOLOK_SMARTAPI_KEY", "GOLOK_SMARTAPI_PUBLIC_IP",
                 "GOLOK_SMARTAPI_LOCAL_IP", "GOLOK_SMARTAPI_MAC")
_SESSION_LOCK = Lock()
_SESSIONS = {}


def _session_identity():
    values = tuple(environ.get(name, "") for name in _IDENTITY_ENV)
    if not all(0 < len(value) <= 128 for value in values):
        raise ProviderError("LOCAL_CREDENTIALS_REQUIRED")
    return hashlib.sha256(repr(values).encode()).digest()


def cached_client(dbname):
    """Called under _SESSION_LOCK by every consumer."""
    if environ.get("GOLOK_SMARTAPI_AUTHORIZED") != "1":
        _SESSIONS.pop(dbname, None)
        raise ProviderError("LOCAL_AUTHORIZATION_REQUIRED")
    cached = _SESSIONS.get(dbname)
    if cached and datetime.now(timezone.utc) < cached[0] and monotonic() < cached[1]:
        try:
            if cached[2] == _session_identity():
                return cached[3]
        except ProviderError:
            _SESSIONS.pop(dbname, None)
            raise
    _SESSIONS.pop(dbname, None)
    raise ProviderError("AUTH_REQUIRED")


class ProviderBudget(models.Model):
    _name = "golok.lab.provider.budget"
    _description = "Read-only provider request budget"
    _log_access = False

    name = fields.Char(required=True)
    next_at = fields.Datetime(required=True)
    _identity = models.Constraint("UNIQUE(name)", "Provider budget already exists.")

    def _reserve_auth(self):
        return self._reserve("authenticate")

    def _reserve(self, operation):
        intervals = {"authenticate": 60, "history": 60, "quote": 60, "upstox_history": 60}
        keys = {"authenticate": "smartapi_auth", "history": "smartapi_history", "quote": "smartapi_quote",
                "upstox_history": "upstox_history"}
        if operation not in intervals:
            return False
        # A failed call still consumes a slot in this database.
        try:
            with self.env.registry.cursor() as cursor:
                cursor.execute("SET LOCAL lock_timeout = '1s'")
                cursor.execute("""
                    INSERT INTO golok_lab_provider_budget (name, next_at)
                    VALUES (%s, (clock_timestamp() AT TIME ZONE 'UTC') + make_interval(secs => %s))
                    ON CONFLICT (name) DO UPDATE SET next_at = EXCLUDED.next_at
                    WHERE golok_lab_provider_budget.next_at <= (clock_timestamp() AT TIME ZONE 'UTC')
                    RETURNING id
                """, (keys[operation], intervals[operation]))
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

    @api.model_create_multi
    def create(self, vals_list):
        if any(vals for vals in vals_list):
            raise ValidationError(_("Diagnostics are computed by the server."))
        return super(ProviderSetup, self.with_context({})).create(vals_list)

    def write(self, vals):
        if vals:
            raise ValidationError(_("Run a diagnostic action to update the result."))
        return super().write(vals)

    def _check_setup_rights(self):
        self.ensure_one()
        self.check_access("write")
        if not self.env.user.has_group(_ADMIN):
            raise AccessError(_("Only Trading System Administrators may diagnose the provider."))

    def _finish(self, status, details):
        super().write({"status": status, "details": details, "checked_at": fields.Datetime.now()})
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
            "Local configuration is present. Confirm entitlement and registered egress, then supply a fresh timestamped TOTP."
        )

    def action_check_configuration(self):
        self._check_setup_rights()
        configuration = self._configuration()
        status, details = configuration[2:]
        return self._finish(status, details + _(" Adapter capabilities: %s.", ", ".join(sorted(CAPABILITIES))))

    def action_test_authentication(self):
        self._check_setup_rights()
        dbname = self.env.cr.dbname
        if not _SESSION_LOCK.acquire(blocking=False):
            return self._finish("BUSY", _("A provider operation is already in progress."))
        try:
            try:
                cached_client(dbname)
            except ProviderError:
                pass
            else:
                return self._finish("AUTHENTICATED", _("The current worker already has an active read-only session."))
            client, credentials, status, details = self._configuration()
            if not client:
                return self._finish(status, details)
            now = datetime.now(timezone.utc)
            if not session_policy.fresh(credentials[2], environ.get("GOLOK_SMARTAPI_TOTP_ISSUED_AT"), now):
                return self._finish("AUTHORIZATION REQUIRED", _("Supply a fresh operator-issued TOTP and its offset-aware issue time."))
            if not self.env["golok.lab.provider.budget"]._reserve_auth():
                return self._finish("RATE LIMITED", _("Wait for the database authentication budget and use a fresh TOTP."))
            try:
                identity = _session_identity()
                client.authenticate(*credentials)
            except ProviderError:
                return self._finish(client.state, _("Authentication could not be verified. Check local settings and broker access."))
            if len(_SESSIONS) >= 8:
                _SESSIONS.pop(next(iter(_SESSIONS)))
            _SESSIONS[dbname] = (session_policy.deadline(now), monotonic() + session_policy.MAX_AGE.total_seconds(),
                                 identity, client)
        finally:
            _SESSION_LOCK.release()
        return self._finish("AUTHENTICATED", _("The read-only session is available in the current worker."))
