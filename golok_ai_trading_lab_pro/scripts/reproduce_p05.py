"""Reproduce and reconcile the public synthetic portfolio fixture."""

import json
import sys
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from services import calendar, experiments, market_data, portfolio


def fixture():
    directory = ROOT / "tests/fixtures/p02"
    spec = json.loads((directory / "spec.json").read_text())
    sessions = calendar.load_schedule(json.dumps(spec["schedule"]))
    bars = tuple(market_data.parse_csv((directory / "candles.csv").read_bytes(),
                                      as_of=datetime(2024, 2, 1, tzinfo=timezone.utc), temporal=True))
    cost = experiments.read_tariffs(json.dumps(spec["tariffs"]))
    day = date(2024, 1, 2)
    series = tuple(portfolio.Series(f"NSE:FIXTURE{index}", "NSE", Decimal(".05"), bars, sessions)
                   for index in range(1, 4))
    return series, day, cost


def run():
    series, day, cost = fixture()
    policy = portfolio.PortfolioPolicy(daily_loss=Decimal(".0026"))
    result = portfolio.replay(series, day, day, 300, ("ST-01",), cost, portfolio_policy=policy, target_policy="fixed_4r")
    assert result == portfolio.replay(series[::-1], day, day, 300, ("ST-01",), cost,
                                      portfolio_policy=policy, target_policy="fixed_4r")
    balance = Decimal("50000")
    for row in result["ledger"]:
        balance += row["delta"]
        assert balance == row["cash"] >= 0
    assert balance == result["ending_cash"]
    assert result["gross"] - result["fees"] == result["net"] == balance - Decimal("50000")
    assert any(row["state"] == "NO_TRADE" and not row["gates"]["G11"]["passed"] for row in result["decisions"])
    return {"calculation": result, "reconciliation": "PASS"}


if __name__ == "__main__":
    print(json.dumps(run(), default=str, indent=2, sort_keys=True))
