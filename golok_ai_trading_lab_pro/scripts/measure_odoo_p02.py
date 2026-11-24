"""Bounded end-to-end ORM benchmark on synthetic OHLCV."""

import json
from datetime import datetime, timezone
from time import perf_counter, process_time

import psutil

from odoo import sql_db
from odoo.addons.golok_ai_trading_lab_pro.services import calendar, market_data


def run(env):
    if not env.cr.dbname.startswith(("golok_p02_migration_", "golok_p03_migration_")):
        raise ValueError("Use the disposable migration harness.")
    available = psutil.virtual_memory().available
    if available < 1024 ** 3:
        raise RuntimeError("The benchmark needs at least 1 GiB immediately available RAM.")
    process = psutil.Process()
    initial_rss = peak_rss = process.memory_info().rss
    company = env["res.company"].create({"name": "Synthetic P02 benchmark"})
    day = "2024-01-02"
    schedule = json.dumps([{"date": day, "kind": "regular", "open": "09:15", "close": "15:30",
                            "entry_cutoff": "14:30", "exit_cutoff": "15:25"}])
    revision = env["golok.lab.calendar"].create({
        "name": "Benchmark calendar", "company_id": company.id, "source": "Synthetic benchmark",
        "exchange": "NSE", "verification": "fixture", "verified_on": day, "schedule": schedule,
    })
    slots = next(iter(calendar.load_schedule(schedule).values())).slots(300)
    raw = (",".join(market_data.TEMPORAL_COLUMNS) + "\n" + "\n".join(
        f"{close.isoformat()},100,103,99,101,1000,{start.isoformat()},{close.isoformat()}" for start, close in slots
    )).encode()
    start, cpu, queries = perf_counter(), process_time(), sql_db.sql_counter
    instruments = env["golok.lab.instrument"].create([
        {"name": f"Synthetic {index}", "symbol": f"P02BENCH{index:02}", "company_id": company.id}
        for index in range(50)
    ])
    datasets = env["golok.lab.dataset"].create([
        {"name": record.name, "instrument_id": record.id, "company_id": company.id, "origin": "synthetic",
         "source": "Synthetic benchmark", "interval": "5m", "calendar_id": revision.id}
        for record in instruments
    ])
    ingestion = perf_counter()
    for dataset in datasets:
        bars = market_data.parse_csv(raw, as_of=datetime.now(timezone.utc), temporal=True)
        assert dataset._import_bars(bars) == len(slots)
        peak_rss = max(peak_rss, process.memory_info().rss)
    ingested = perf_counter()
    runs = env["golok.lab.run"]
    cutoff = slots[-1][1].replace(tzinfo=None)
    for dataset in datasets:
        result = runs.create({"dataset_id": dataset.id, "as_of": cutoff})
        assert result.bar_count == len(slots)
        peak_rss = max(peak_rss, process.memory_info().rss)
    researched = perf_counter()
    env.flush_all()
    count_start = perf_counter()
    count = env["golok.lab.candle"].search_count([("company_id", "=", company.id)])
    count_seconds = perf_counter() - count_start
    env.cr.commit()
    assert count == 50 * len(slots)
    wall_seconds = perf_counter() - start
    cpu_seconds = process_time() - cpu
    print(json.dumps({
        "dataset": "synthetic", "instruments": 50, "bars_per_instrument": len(slots), "rows": count,
        "csv_bytes": 50 * len(raw), "wall_seconds": wall_seconds, "cpu_seconds": cpu_seconds,
        "average_process_cpu_percent_single_core": cpu_seconds / wall_seconds * 100,
        "ingestion_seconds": ingested - ingestion, "research_seconds": researched - ingested,
        "company_count_query_seconds": count_seconds, "odoo_sql_statements": sql_db.sql_counter - queries,
        "process_initial_rss_bytes": initial_rss, "process_max_sampled_rss_bytes": peak_rss,
        "system_start_available_bytes": available, "system_end_available_bytes": psutil.virtual_memory().available,
    }, sort_keys=True))
