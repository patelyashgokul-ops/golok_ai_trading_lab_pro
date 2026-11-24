"""Run from Odoo shell against a disposable harness database."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from queue import Queue
from time import monotonic, sleep

from psycopg2.errors import UniqueViolation

from odoo import SUPERUSER_ID, api
from odoo.addons.golok_ai_trading_lab_pro.services.market_data import parse_bar


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
    registry, dataset_id = env.registry, dataset.id
    bar = parse_bar("2024-01-02T09:20:00+05:30", "100", "102", "99", "101", "1000",
                    as_of=datetime.now(timezone.utc))
    follower_pid = Queue(maxsize=1)

    def compete():
        with registry.cursor() as cursor:
            cursor.execute("SET LOCAL statement_timeout = '8s'")
            cursor.execute("SELECT pg_backend_pid()")
            follower_pid.put(cursor.fetchone()[0])
            contender = api.Environment(cursor, SUPERUSER_ID, {})["golok.lab.dataset"].browse(dataset_id)
            try:
                contender._import_bars([bar])
            except UniqueViolation:
                cursor.rollback()
                return "unique constraint rejected the overlapping import"
            raise AssertionError("The competing importer was expected to hit the unique constraint.")

    env.cr.execute("SELECT pg_backend_pid()")
    lead_pid = env.cr.fetchone()[0]
    assert dataset._import_bars([bar]) == 1
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(compete)
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
        print(f"PASS: independent PostgreSQL connections overlapped and {future.result(timeout=8)}")
    assert dataset._import_bars([bar]) == 0
    assert env["golok.lab.candle"].search_count([("dataset_id", "=", dataset.id)]) == 1
    print("PASS: a new transaction replayed the identical import with one total stored candle")
