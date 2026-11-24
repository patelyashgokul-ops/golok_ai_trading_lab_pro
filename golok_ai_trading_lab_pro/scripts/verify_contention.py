"""Run from Odoo shell against a disposable harness database."""

import json
import subprocess
import sys
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
    if env.cr.dbname.startswith(("golok_p08_fresh_", "golok_p09_fresh_")):
        _interrupt_job(env, runner, dataset)
    if env.cr.dbname.startswith("golok_p09_fresh_"):
        _p09_races(env, runner, dataset, tariff)


def _p09_races(env, runner, dataset, tariff):
    scope = {"allowed_company_ids": [dataset.company_id.id]}
    administrator = new_test_user(env, login="golok-cycle-race", groups="golok_ai_trading_lab_pro.group_admin",
                                  company_id=dataset.company_id.id, company_ids=[(6, 0, [dataset.company_id.id])])
    watch = env(user=administrator.id, context=scope)["golok.lab.session.watch"].create({"dataset_id": dataset.id})
    account = runner["golok.lab.fixture.account"].create({"name": "Independent fixture order test", "tariff_id": tariff.id})
    env.cr.commit()
    at = datetime(2024, 1, 2, 4, 5, tzinfo=timezone.utc)
    watch._dispatch(at)
    with env.registry.cursor() as other:
        peer = api.Environment(other, administrator.id, scope)["golok.lab.session.watch"].browse(watch.id)
        assert env.cr is not other
        assert not peer._dispatch(at)
    env.cr.commit()
    assert runner["golok.lab.research.cycle"].search_count([("watch_id", "=", watch.id)]) == 1
    print("PASS: a concurrent scheduler skipped the locked watch and only one observation cycle was queued")

    def account_for(other):
        return other(user=runner.uid, context=scope)[account._name].browse(account.id)

    def reserve(other):
        account_for(other).action_reserve_fixture()
        other.flush_all()

    def close(other):
        account_for(other).action_close_fixture()
        other.flush_all()

    _overlap(env, lambda: reserve(env), reserve, (SerializationFailure, ValidationError))
    account.action_open_fixture()
    env.cr.commit()
    _overlap(env, lambda: close(env), close, SerializationFailure)
    account.action_close_fixture()
    account.invalidate_recordset()
    assert len(account.order_ids) == 1 and account.order_ids.state == "closed"
    assert account.journal_ids.mapped("kind") == ["reserved", "opened", "closed"]
    assert account.available == account.opening + account.realized
    print("PASS: independent fixture reservation and closure races left one order, one fill per side and a reconciled journal")
    _interrupt_fixture_exit(env, account)


def _interrupt_fixture_exit(env, account):
    from odoo.cli import shell

    account.action_reserve_fixture()
    account.action_open_fixture()
    order = account.order_ids[:1]
    env.cr.execute("SELECT inet_server_port()")
    port = str(env.cr.fetchone()[0])
    env.cr.commit()
    root = Path(shell.__file__).resolve().parents[2]
    addons = Path(__file__).resolve().parents[2]
    process = subprocess.Popen([
        sys.executable, "-B", str(root / "odoo-bin"), "shell", "--no-http", "-d", env.cr.dbname,
        "--db_host=127.0.0.1", "--db_user=golok_test", f"--db_port={port}",
        f"--addons-path={root / 'addons'},{addons}", "--data-dir=.local-test/odoo-data",
        "--logfile=.local-test/p09-fixture-worker.log",
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    try:
        process.stdin.write(
            f"from time import sleep\n"
            f"account = env(user={account.env.uid}, context={{'allowed_company_ids': [{account.company_id.id}]}})"
            f"['{account._name}'].browse({account.id})\n"
            "account.action_close_fixture()\n"
            "env.flush_all()\n"
            "print('PAPER_EXIT_WRITTEN', flush=True)\n"
            "sleep(45)\n"
        )
        process.stdin.close()
        with ThreadPoolExecutor(max_workers=1) as executor:
            try:
                assert executor.submit(process.stdout.readline).result(timeout=22).strip() == "PAPER_EXIT_WRITTEN"
            finally:
                process.kill()
                process.wait(timeout=5)
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        process.stdout.close()
    env.invalidate_all()
    assert order.state == "open" and "closed" not in account.journal_ids.filtered(lambda event: event.order_id == order).mapped("kind")
    account.action_close_fixture()
    assert order.state == "closed"
    assert account.journal_ids.filtered(lambda event: event.order_id == order).mapped("kind") == ["reserved", "opened", "closed"]
    assert account.available == account.opening + account.realized
    env.cr.commit()
    print("PASS: actual fixture closing worker was terminated after uncommitted writes and one retry reconciled the exit")


def _interrupt_job(env, runner, dataset):
    job = runner["golok.lab.research.job"].create({"dataset_id": dataset.id, "cutoff": "2024-01-02 04:20:00"})
    job_id = job.id
    env.cr.execute("SELECT inet_server_port()")
    port = str(env.cr.fetchone()[0])
    env.cr.commit()
    worker = Path(__file__).with_name("hold_research_claim.py")
    process = subprocess.Popen([sys.executable, "-B", str(worker), env.cr.dbname, port, str(job_id)],
                               stdout=subprocess.PIPE, text=True)
    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            try:
                assert executor.submit(process.stdout.readline).result(timeout=12).strip() == "CLAIMED"
                with env.registry.cursor() as cursor:
                    jobs = api.Environment(cursor, SUPERUSER_ID, {})["golok.lab.research.job"]
                    jobs._cron_run_next()
                    assert jobs.browse(job_id).state == "queued"
            finally:
                process.kill()
                process.wait(timeout=5)
    finally:
        process.stdout.close()
    for _ in range(20):
        with env.registry.cursor() as cursor:
            fresh = api.Environment(cursor, SUPERUSER_ID, {})
            jobs = fresh["golok.lab.research.job"]
            jobs._cron_run_next()
            recovered = jobs.browse(job_id)
            if recovered.state == "completed":
                assert recovered.run_id
                result_id = recovered.run_id.id
                cursor.commit()
                break
        sleep(0.1)
    else:
        raise AssertionError("An interrupted claim did not recover.")
    with env.registry.cursor() as cursor:
        fresh = api.Environment(cursor, SUPERUSER_ID, {})
        jobs = fresh["golok.lab.research.job"]
        jobs._cron_run_next()
        assert jobs.browse(job_id).run_id.id == result_id
        assert fresh["golok.lab.run"].search_count([("dataset_id", "=", dataset.id),
                                                   ("as_of", "=", "2024-01-02 04:20:00")]) == 1
    print("PASS: independent worker skipped a locked job, forced worker kill rolled back and retry produced exactly one result")
    _recover_committed_lease(env, runner, dataset)


def _recover_committed_lease(env, runner, dataset):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    job = runner["golok.lab.research.job"].create({"dataset_id": dataset.id, "cutoff": "2024-01-02 04:25:00"})
    job_id = job.id
    env.cr.commit()
    with env.registry.cursor() as cursor:
        jobs = api.Environment(cursor, SUPERUSER_ID, {})["golok.lab.research.job"]
        claimed = jobs._claim_job(now)
        assert claimed.id == job_id and claimed.attempts == 1
        old_token = claimed.worker_token
        cursor.commit()
    with env.registry.cursor() as cursor:
        jobs = api.Environment(cursor, SUPERUSER_ID, {})["golok.lab.research.job"]
        assert not jobs._claim_job(now + timedelta(minutes=1))
        reclaimed = jobs._claim_job(now + timedelta(minutes=6))
        assert reclaimed.id == job_id and reclaimed.attempts == 2
        token = reclaimed.worker_token
        assert token != old_token
        cursor.commit()
    with env.registry.cursor() as cursor:
        jobs = api.Environment(cursor, SUPERUSER_ID, {})["golok.lab.research.job"]
        jobs._run_claim(job_id, old_token)
        assert jobs.browse(job_id).state == "claimed"
        jobs._run_claim(job_id, token)
        cursor.commit()
    with env.registry.cursor() as cursor:
        fresh = api.Environment(cursor, SUPERUSER_ID, {})
        jobs = fresh["golok.lab.research.job"]
        jobs._run_claim(job_id, token)
        assert jobs.browse(job_id).state == "completed"
        assert fresh["golok.lab.run"].search_count([("dataset_id", "=", dataset.id),
                                                   ("as_of", "=", "2024-01-02 04:25:00")]) == 1
    print("PASS: a committed lease was recovered once after expiry and stale worker token was denied")
