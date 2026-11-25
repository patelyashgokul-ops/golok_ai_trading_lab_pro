"""Dedicated Odoo-shell worker for authorized Upstox V3 LTPC capture."""

from contextlib import closing
from os import environ
from time import monotonic, sleep

from odoo import SUPERUSER_ID, api, fields
from odoo.exceptions import AccessError, ValidationError
from psycopg2.errors import DeadlockDetected, SerializationFailure

from odoo.addons.golok_ai_trading_lab_pro.models.sync import _ADMIN
from odoo.addons.golok_ai_trading_lab_pro.services import upstox_analytics
from odoo.addons.golok_ai_trading_lab_pro.services.smartapi import ProviderError


def _state(env, company, *, locked=False):
    if locked:
        env.cr.execute("SELECT id FROM golok_lab_analytics_config WHERE company_id=%s FOR UPDATE", [company])
    record = env["golok.lab.analytics.config"].sudo().search([("company_id", "=", company)], limit=1)
    user = record.operator_id
    if not (record.enabled and record.collect and record.worker_capture and user.active
            and record.company_id in user.company_ids and user.has_group(_ADMIN)):
        raise ProviderError("WORKER_DISABLED")
    service = record.with_user(user).with_context(allowed_company_ids=[company])
    return service, record


def _signature(record, review, session):
    return (record.id, record.envelope, record.expires_at, record.operator_id.id,
            record.mapping_id.id, record.calendar_id.id, review.id, session.day)


def _window(registry, company, *, updates=upstox_analytics.stream_updates):
    def transaction(callback, *, write=False):
        with registry.cursor() as cursor:
            result = callback(api.Environment(cursor, SUPERUSER_ID, {}))
            if write:
                cursor.commit()
            return result

    def begin(env):
        service, record = _state(env, company)
        now = fields.Datetime.now()
        if record.next_collection and record.next_collection > now:
            raise ProviderError("COOLDOWN")
        review, mapping, session = service._stream_scope(record, now)
        return record._credential(), mapping.token, mapping.isin, _signature(record, review, session)

    signature = None
    status = None
    checks_until = 0
    last_tick = None

    def current(env, *, locked=False):
        service, record = _state(env, company, locked=locked)
        if not record.expires_at or record.expires_at <= fields.Datetime.now():
            raise ProviderError("LOCAL_CREDENTIALS_REQUIRED")
        review, mapping, session = service._stream_scope(record, fields.Datetime.now())
        if _signature(record, review, session) != signature:
            raise ProviderError("WORKER_CONFIGURATION_CHANGED")
        return service, record, review, mapping, session

    def active():
        nonlocal checks_until
        now = monotonic()
        if now >= checks_until:
            transaction(current)
            checks_until = now + 2
        return True

    def consume(env, point):
        service, record, review, mapping, session = current(env, locked=True)
        service._store_worker_sample(record, review, mapping, session, point)

    try:
        token, key, isin, signature = transaction(begin)
        reserve = lambda operation: transaction(lambda env: env["golok.lab.provider.budget"]._reserve(operation))
        with closing(updates(token, key, isin, reserve, active=active)) as observations:
            for point in observations:
                tick = (point["event"], point["price"])
                if tick != last_tick:
                    transaction(lambda env: consume(env, point), write=True)
                    last_tick = tick
        status = None if last_tick else "STALE_OR_UNAVAILABLE"
    except (ValidationError, AccessError):
        status = "PERMISSION_OR_HOLDOUT_BLOCKED"
    except ProviderError as exc:
        status = str(exc)
    finally:
        if status and status not in {"COOLDOWN", "WORKER_DISABLED", "WORKER_CONFIGURATION_CHANGED"}:
            def failure(env):
                try:
                    service, record = _state(env, company, locked=True)
                except ProviderError:
                    return
                if signature and (record.id, record.envelope, record.expires_at, record.operator_id.id,
                                  record.mapping_id.id, record.calendar_id.id) != signature[:6]:
                    return
                service._stream_failure(record, fields.Datetime.now(), status)
            transaction(failure, write=True)


def run(env):
    company = int(environ["GOLOK_ANALYTICS_COMPANY_ID"])
    if company <= 0 or company >= 2**31:
        raise ValueError("Supply a valid Odoo company ID.")
    registry = env.registry
    env.cr.rollback()
    with registry.cursor() as owner:
        owner.execute("SELECT pg_try_advisory_lock(%s, %s)", [1_702_128_917, company])
        if not owner.fetchone()[0]:
            raise RuntimeError("An Analytics worker already owns this company.")
        try:
            owner.commit()
            print("Upstox capture worker started for the configured company.", flush=True)
            while True:
                try:
                    _window(registry, company)
                except (SerializationFailure, DeadlockDetected):
                    pass
                sleep(3)
        except KeyboardInterrupt:
            print("Upstox capture worker stopped.", flush=True)
        finally:
            owner.execute("SELECT pg_advisory_unlock(%s, %s)", [1_702_128_917, company])
            owner.commit()
