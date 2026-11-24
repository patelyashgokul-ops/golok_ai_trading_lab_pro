"""Measure deterministic service workloads on synthetic inputs."""

import sys
import time
import tracemalloc
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.market_data import parse_csv
from services.research import describe


def fixture(count):
    start = datetime(2024, 1, 2, 3, 50, tzinfo=timezone.utc)
    rows = (
        f"{(start + timedelta(minutes=i)).isoformat()},100,102,99,101,{i + 100}\n"
        for i in range(count)
    )
    return ("close_time,open,high,low,close,volume\n" + "".join(rows)).encode()


def measure(instruments, rows_per_instrument):
    raw = fixture(rows_per_instrument)
    as_of = datetime(2025, 1, 1, tzinfo=timezone.utc)
    parse_time = research_time = 0
    tracemalloc.start()
    wall_started = time.perf_counter()
    cpu_started = time.process_time()
    for _ in range(instruments):
        started = time.perf_counter()
        bars = parse_csv(raw, as_of=as_of)
        parsed = time.perf_counter()
        values = describe(bars[-250:])
        parse_time += parsed - started
        research_time += time.perf_counter() - parsed
        assert values["sma20"] == 101
    cpu_seconds = time.process_time() - cpu_started
    wall_seconds = time.perf_counter() - wall_started
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{instruments},{rows_per_instrument},{wall_seconds:.4f},{cpu_seconds:.4f},"
          f"{parse_time:.4f},{research_time:.4f},{peak}")


if __name__ == "__main__":
    print("instruments,rows_per_instrument,wall_s,cpu_s,parse_s,research_s,peak_traced_bytes")
    for count in (50, 100, 250, 500):
        measure(count, 250)
    measure(1, 4000)
