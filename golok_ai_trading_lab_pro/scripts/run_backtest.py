"""Run a single reproducible ST-01 synthetic experiment."""

import argparse
import json
import sys
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services import backtest, calendar, market_data
from services.simulation import CostSchedule, Tariff


def load_file(path, limit):
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise ValueError(f"{path.name} exceeds its input size limit.")
    return raw


def run(spec_path, bars_path):
    spec_raw = load_file(spec_path, 96 * 1024)
    spec = json.loads(spec_raw)
    session = calendar.load_schedule(json.dumps(spec["schedule"]))[date.fromisoformat(spec["date"])]
    bars = market_data.parse_csv(load_file(bars_path, market_data.MAX_BYTES),
                                 as_of=datetime.now(timezone.utc), temporal=True)
    tariffs = []
    for tariff in spec["tariffs"]:
        tariff = {**tariff, "starts": date.fromisoformat(tariff["starts"]),
                  "ends": date.fromisoformat(tariff["ends"]) if tariff.get("ends") else None}
        for field in ("amount", "minimum", "maximum"):
            if tariff.get(field) is not None:
                tariff[field] = Decimal(tariff[field])
        tariffs.append(Tariff(**tariff))
    return backtest.replay(bars, session, spec["exchange"], market_data.INTERVALS[spec["interval"]],
                           Decimal(spec["tick"]), CostSchedule(tariffs), source=spec["source"],
                           origin=spec["origin"], partition=spec["partition"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("specification", type=Path)
    parser.add_argument("candles", type=Path)
    arguments = parser.parse_args()
    try:
        print(json.dumps(run(arguments.specification, arguments.candles), default=str, indent=2, sort_keys=True))
    except (ValueError, TypeError, KeyError, ArithmeticError, OSError) as exc:
        parser.exit(2, f"Experiment rejected: {exc}\n")
