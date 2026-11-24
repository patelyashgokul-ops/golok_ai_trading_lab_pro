"""Reproduce five strategy outcomes on identical synthetic inputs and higher fees."""

import json
import sys
from dataclasses import replace
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.reproduce_p05 import fixture
from services import performance, portfolio, simulation, strategies, targets


def run():
    assets, day, costs = fixture()
    stressed = simulation.CostSchedule([replace(rule, amount=rule.amount * 2) for rule in costs.tariffs])
    scenarios = {}
    for label, tariff in (("baseline", costs), ("double_tariff_rates", stressed)):
        rows = {}
        for code in sorted(strategies.REGISTRY):
            result = portfolio.replay(assets, day, day, 300, (code,), tariff, target_policy="fixed_4r")
            gross, fees, net = (result[key] for key in ("gross", "fees", "net"))
            assert gross - fees == net == result["ending_cash"] - Decimal("50000")
            assert sum(row["delta"] for row in result["ledger"]) == net
            rows[code] = {"net": net, "gross": gross, "fees": fees, "trades": len(result["trades"]),
                          "considered": len(result["decisions"]), "suspended": result["suspended"]}
        scenarios[label] = rows
    return {"origin": "synthetic", "date": day, "assets": [asset.key for asset in assets],
            "scenarios": scenarios, "financial_eligibility": "INSUFFICIENT"}


if __name__ == "__main__":
    if sys.argv[1:] == ["--level-policies"]:
        assets, day, costs = fixture()
        codes = tuple(strategies.REGISTRY)
        policies = {}
        for policy in targets.POLICIES:
            result = portfolio.replay(assets, day, day, 300, codes, costs, target_policy=policy)
            assert result == portfolio.replay(assets[::-1], day, day, 300, codes[::-1], costs, target_policy=policy)
            policies[policy] = {"trades": result["trades"], "decisions": result["decisions"],
                                "metrics": performance.summarize(result)}
        print(json.dumps(policies, default=str, indent=2))
    elif len(sys.argv) == 1:
        print(json.dumps(run(), default=str, indent=2))
    else:
        raise SystemExit("Usage: reproduce_p06.py [--level-policies]")
