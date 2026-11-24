"""Generate redistributable synthetic replay and cash journal evidence."""

import json
import sys
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from services import calendar, experiments, market_data, paper, simulation


def reproduce():
    fixture = ROOT / "tests/fixtures/p02"
    spec = json.loads((fixture / "spec.json").read_text())
    raw = (fixture / "candles.csv").read_bytes()
    _, second = raw.split(b"\n", 1)
    sequence = raw.rstrip() + b"\n" + second.replace(b"2024-01-02", b"2024-01-03")
    bars = market_data.parse_csv(sequence, as_of=datetime(2024, 2, 1, tzinfo=timezone.utc), temporal=True)
    sessions = calendar.load_schedule(json.dumps([*spec["schedule"], {**spec["schedule"][0], "date": "2024-01-03"}]))
    output = experiments.simulate(
        bars, sessions, date(2024, 1, 2), date(2024, 1, 3), "NSE", 300, Decimal("0.05"),
        experiments.read_tariffs(json.dumps(spec["tariffs"])), "Public synthetic P03 correctness fixture", simulation.RiskPolicy(),
    )
    closing, ledger = paper.postings(output["trades"], 5_000_000)
    assert closing == 5_000_000 + sum(row["cash_delta"] for row in ledger)
    assert sum(row["reserved_delta"] for row in ledger) == sum(row["quantity_delta"] for row in ledger) == 0
    assert output["status"] == "completed" and output["metrics"]["trades"] == 2
    return {"experiment": output, "virtual_journal": ledger, "opening_paise": 5_000_000, "closing_paise": closing}


if __name__ == "__main__":
    print(json.dumps(reproduce(), default=str, indent=2, sort_keys=True))
