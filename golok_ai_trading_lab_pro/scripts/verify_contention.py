"""Run from Odoo shell against a disposable harness database."""

import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from queue import Queue
from time import monotonic, sleep

from psycopg2.errors import ExclusionViolation, SerializationFailure, UniqueViolation

from odoo import SUPERUSER_ID, api
from odoo.exceptions import ValidationError
from odoo.tests.common import new_test_user
from odoo.addons.golok_ai_trading_lab_pro.services.market_data import parse_bar, parse_csv


def run(env):
    if not env.cr.dbname.startswith("golok_"):
        raise ValueError("A disposable golok_ database is required.")
    company = env["res.company"].create({"name": "Synthetic contention test"})
    instrument = env["golok.lab.instrument"].create({
        "name": "Concurrency Fixture", "symbol": "CONTENTION", "company_id": company.id,
    })
    dataset = env["golok.lab.dataset"].create({
        "name": "Synthetic contention CSV", "source": "Concurrency test", "origin": "synthetic",
        "instrument_id": instrument.id, "interval": "5m", "company_id": company.id,
    })
    env.cr.commit()
    dataset_id = dataset.id
    bar = parse_bar("2024-01-02T09:20:00+05:30", "100", "102", "99", "101", "1000",
                    as_of=datetime.now(timezone.utc))
    _race(env, dataset, dataset_id, bar, [bar])
    assert dataset._import_bars([bar]) == 0
    assert env["golok.lab.candle"].search_count([("dataset_id", "=", dataset.id)]) == 1
    print("PASS: a new transaction replayed the identical import with one total stored candle")

    second = replace(bar, close_time=bar.close_time + timedelta(minutes=5))
    third = replace(bar, close_time=bar.close_time + timedelta(minutes=10))
    conflicting = replace(second, close=Decimal("101.50"))
    _race(env, dataset, dataset_id, second, [third, conflicting])
    candles = env["golok.lab.candle"].search([("dataset_id", "=", dataset.id)], order="close_time")
    assert [record._to_bar() for record in candles] == [bar, second]
    try:
        dataset._import_bars([third, conflicting])
    except ValidationError:
        assert dataset._import_bars([second, third]) == 1
    else:
        raise AssertionError("Stored value conflict was not detected after reloading.")
    assert env["golok.lab.candle"].search_count([("dataset_id", "=", dataset.id)]) == 3
    env.cr.commit()
    print("PASS: conflicting overlap rolled back a nonconflicting row from the same batch and retry succeeded")
    _p03_races(env, company, instrument)


def _race(env, dataset, dataset_id, lead, requests):
    def lead_insert():
        assert dataset._import_bars([lead]) == 1

    def compete(other):
        other["golok.lab.dataset"].browse(dataset_id)._import_bars(requests)

    _overlap(env, lead_insert, compete, UniqueViolation)
    print("PASS: independent PostgreSQL connections overlapped and unique constraint rejected the overlapping import")


def _overlap(env, lead, compete, expected_error):
    follower_pid = Queue(maxsize=1)

    def follower():
        with env.registry.cursor() as cursor:
            cursor.execute("SET LOCAL statement_timeout = '8s'")
            cursor.execute("SELECT pg_backend_pid()")
            follower_pid.put(cursor.fetchone()[0])
            try:
                compete(api.Environment(cursor, SUPERUSER_ID, {}))
            except expected_error:
                cursor.rollback()
                return
            raise AssertionError("The competing transaction was expected to be rejected.")

    env.cr.execute("SELECT pg_backend_pid()")
    lead_pid = env.cr.fetchone()[0]
    lead()
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(follower)
        try:
            other_pid = follower_pid.get(timeout=3)
            deadline = monotonic() + 4
            while monotonic() < deadline:
                env.cr.execute("SELECT %s = ANY(pg_blocking_pids(%s))", (lead_pid, other_pid))
                if env.cr.fetchone()[0]:
                    break
                sleep(0.05)
            else:
                raise AssertionError("No overlapping insert lock was observed.")
            env.cr.commit()
        except Exception:
            env.cr.rollback()
            raise
        future.result(timeout=8)


def _p03_races(env, company, instrument):
    mapping = {"company_id": company.id, "instrument_id": instrument.id, "symbol": "CONTENTION",
               "provider": "manual", "token": "271", "starts": "2024-01-01", "ends": "2024-02-01",
               "tick": "0.05", "lot": 1, "listing_status": "listed", "source": "Synthetic concurrency",
               "revision": "race-1", "verification": "fixture"}
    _overlap(env, lambda: env["golok.lab.mapping"].create(mapping),
             lambda follower: follower["golok.lab.mapping"].create({**mapping, "starts": "2024-01-15"}),
             ExclusionViolation)
    print("PASS: independent transactions contended on the instrument range exclusion")

    fixture = Path(__file__).resolve().parent.parent / "tests/fixtures/p02"
    spec = json.loads((fixture / "spec.json").read_text())
    operator = new_test_user(env, login="golok-paper-race", groups="golok_ai_trading_lab_pro.group_risk",
                             company_id=company.id, company_ids=[(6, 0, [company.id])])
    revision = env["golok.lab.calendar"].create({
        "company_id": company.id, "name": "Race calendar", "source": "Synthetic race", "exchange": "NSE",
        "verification": "fixture", "verified_on": "2024-01-01", "schedule": json.dumps(spec["schedule"]),
    })
    dataset = env["golok.lab.dataset"].create({
        "company_id": company.id, "instrument_id": instrument.id, "calendar_id": revision.id, "interval": "5m",
        "name": "Race replay", "source": "Synthetic replay race", "origin": "synthetic",
    })
    dataset._import_bars(parse_csv((fixture / "candles.csv").read_bytes(), as_of=datetime.now(timezone.utc), temporal=True))
    tariff = env["golok.lab.tariff"].create({"name": "Replay race fees", "company_id": company.id,
                                             "lines": json.dumps(spec["tariffs"])})
    actor, scope = operator.id, {"allowed_company_ids": [company.id]}
    runner = env(user=actor, context=scope)
    experiment = runner["golok.lab.experiment"].create({
        "dataset_id": dataset.id, "strategy_id": env.ref("golok_ai_trading_lab_pro.strategy_st01_p05").id,
        "tariff_id": tariff.id, "starts": "2024-01-02", "ends": "2024-01-02", "capital": "50000", "tick": "0.05",
    })
    account = runner["golok.lab.paper.account"].create({"name": "Replay collision fixture"})
    account_id, experiment_id = account.id, experiment.id
    env.cr.commit()

    def post(other):
        scoped = other(user=actor, context=scope)
        return scoped["golok.lab.paper.account"].browse(account_id)._post_replay(
            scoped["golok.lab.experiment"].browse(experiment_id)
        )

    _overlap(env, lambda: post(env), post, SerializationFailure)
    batch = post(env)
    assert env["golok.lab.paper.batch"].search_count([("account_id", "=", account_id)]) == 1
    assert len(batch.event_ids) == 3
    assert batch.after_paise == batch.before_paise + sum(batch.event_ids.mapped("cash_delta"))
    print("PASS: independent virtual-account postings overlapped; retry found exactly one reconciled batch")
    holdout_calendar = revision.copy({
        "name": "Holdout race calendar", "schedule": json.dumps([
            {**spec["schedule"][0], "date": day} for day in ("2024-01-02", "2024-01-05")])})
    daily = env["golok.lab.dataset"].create({
        "company_id": company.id, "instrument_id": instrument.id, "calendar_id": holdout_calendar.id,
        "interval": "5m", "name": "Holdout race", "source": "Synthetic holdout race", "origin": "synthetic"})
    payload = (fixture / "candles.csv").read_bytes()
    for day in (b"2024-01-02", b"2024-01-05"):
        daily._import_bars(parse_csv(payload.replace(b"2024-01-02", day), as_of=datetime.now(timezone.utc), temporal=True))
    inputs = {"dataset_ids": daily.ids, "tariff_id": tariff.id, "strategy": "ST-01", "tick": "0.05", "capital": "50000"}
    training = runner["golok.lab.portfolio"].create({**inputs, "starts": "2024-01-02", "ends": "2024-01-02"})
    wizard = runner["golok.lab.portfolio.wizard"].create({
        **inputs, "dataset_ids": [(6, 0, daily.ids)], "starts": "2024-01-05", "ends": "2024-01-05", "training_id": training.id})
    seal_id = wizard.action_seal()["res_id"]
    env.cr.commit()

    def consume(other):
        scoped = other(user=actor, context=scope)
        return scoped["golok.lab.holdout"].browse(seal_id).action_consume()

    _overlap(env, lambda: consume(env), consume, SerializationFailure)
    try:
        consume(env)
    except ValidationError:
        pass
    else:
        raise AssertionError("A second consumption unexpectedly succeeded.")
    assert runner["golok.lab.holdout"].browse(seal_id).result_id
    print("PASS: independent holdout evaluations overlapped and a fresh retry rejected repeated consumption")
