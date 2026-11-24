"""Check fixed-operation quota reservations with independent database cursors."""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from odoo import SUPERUSER_ID, api


def run(env):
    if not env.cr.dbname.startswith("golok_p04_migration_"):
        raise ValueError("Use the isolated P04 migration test database.")
    registry = env.registry
    for operation in ("authenticate", "history", "quote"):
        barrier = Barrier(2)

        def reserve():
            with registry.cursor() as cursor:
                budget = api.Environment(cursor, SUPERUSER_ID, {})["golok.lab.provider.budget"]
                barrier.wait(timeout=10)
                return budget._reserve(operation)

        with ThreadPoolExecutor(max_workers=2) as executor:
            jobs = [executor.submit(reserve) for _ in range(2)]
            results = [job.result(timeout=15) for job in jobs]
        assert sorted(results) == [False, True], (operation, results)
        assert not env["golok.lab.provider.budget"]._reserve(operation), operation
        print(f"QUOTA PASS {operation}: two workers, one committed reservation, immediate retry denied")
