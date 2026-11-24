"""Reproduce bounded software stress on the same set of authored observations."""

import json
import sys
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.reproduce_p05 import fixture
from services import portfolio, replay_contract, simulation, strategies


def stress():
    assets, day, costs = fixture()
    codes = tuple(sorted(strategies.REGISTRY))
    policy = "fixed_4r"

    def bars(change):
        return tuple(replace(asset, bars=tuple(change(bar, i) for i, bar in enumerate(asset.bars))) for asset in assets)

    def run(series, schedule=costs, target=policy, ends=day):
        try:
            report = portfolio.replay(series, day, ends, 300, codes, schedule, target_policy=target)
        except ValueError as exc:
            return {"status": "REJECTED", "reason": str(exc)}
        assert report["gross"] - report["fees"] == report["net"]
        assert report["ending_cash"] - report["initial_cash"] == report["net"]
        return {key: report[key] for key in ("gross", "fees", "net", "suspended")} | {"trades": len(report["trades"])}

    def costs_with(rule_change):
        return simulation.CostSchedule([rule_change(rule) for rule in costs.tariffs])

    delayed = tuple(replace(
        asset, origin="historical_contract", bars=tuple(
            replace(bar, available_at=min(bar.close_time + timedelta(minutes=1), asset.sessions[day].closing))
            for bar in asset.bars)) for asset in assets)
    proof = {asset.key: replay_contract.Provenance(
        "historical_intraday", "5m", replay_contract.fingerprint(asset), "verified_publication", True, True, True, True)
        for asset in delayed}
    delay = replay_contract.replay_fixture(delayed, proof, day, day, 300, codes, costs, target_policy=policy)
    cases = {
        "baseline": run(assets),
        "doubled_fees": run(assets, costs_with(lambda rule: replace(rule, amount=rule.amount * 2))),
        "extra_slippage": run(assets, costs_with(lambda rule: replace(rule, amount=rule.amount + Decimal(2))
                                                 if rule.name == "slippage" else rule)),
        "delayed_publication": {"net": delay["net"], "trades": len(delay["trades"]), "scope": delay["scope"]},
        "missed_entry": run(bars(lambda bar, index: replace(bar, open=Decimal(106)) if index == 5 else bar)),
        "adverse_gap": run(bars(lambda bar, index: replace(bar, high=Decimal(110), low=Decimal(100)) if index == 5
                                else replace(bar, open=Decimal(97), low=Decimal(96)) if index == 6 else bar)),
        "lower_volume": run(bars(lambda bar, _index: replace(bar, volume=bar.volume // 10))),
        "missing_observation": run(tuple(replace(asset, bars=asset.bars[:-1]) for asset in assets)),
        "structure_target": run(assets, target="structure"),
        "single_instrument": run(assets[:1]),
        "uncovered_window": run(assets, ends=day + timedelta(days=1)),
    }
    assert cases["missing_observation"]["status"] == "REJECTED"
    assert cases["doubled_fees"]["fees"] >= cases["baseline"]["fees"]
    return {"scope": "SYNTHETIC_SOFTWARE_ONLY", "date": day, "cases": cases}


if __name__ == "__main__":
    print(json.dumps(stress(), default=str, indent=2))
