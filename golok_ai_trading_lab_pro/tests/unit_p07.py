import unittest
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from scripts.reproduce_p05 import fixture
from services import bhavcopy, portfolio, strategies, targets


class P07Tests(unittest.TestCase):
    def test_causal_targets_and_cost_veto(self):
        assets, day, costs = fixture()
        early, later = assets[0].bars[0], assets[0].bars[-1]
        early = replace(early, high=Decimal("103"))
        later = replace(later, high=Decimal("150"))
        self.assertEqual(targets.levels([early, later], Decimal(102), Decimal(99), "structure",
                                       early.close_time + timedelta(seconds=1), later.close_time)[0], (Decimal(103),))
        result = portfolio.replay(assets, day, day, 300, ("ST-01",), costs)
        self.assertFalse(result["trades"])
        self.assertTrue(all(row["state"] == "NO_TRADE" and row["live_actionability"] == "BLOCKED"
                            for row in result["decisions"]))
        self.assertTrue(result["decisions"])

    def test_rank_all_strategies_and_instruments_before_reserving(self):
        assets, day, costs = fixture()
        better = replace(strategies.REGISTRY["ST-02"], signal=lambda bars, session:
                         Decimal("100.05") if len(bars) == 4 else None)
        series = (assets[0], replace(assets[1], bars=tuple(
            replace(bar, volume=bar.volume * 2) for bar in assets[1].bars)))
        config = {"target_policy": "fixed_4r", "portfolio_policy": portfolio.PortfolioPolicy(daily_entries=1)}
        with patch.dict(strategies.REGISTRY, {"ST-02": better}):
            result = portfolio.replay(series, day, day, 300, ("ST-01", "ST-02"), costs, **config)
            backwards = portfolio.replay(series[::-1], day, day, 300, ("ST-02", "ST-01"), costs, **config)
        self.assertEqual(result, backwards)
        self.assertEqual(len(result["decisions"]), 4)
        self.assertEqual(len(result["trades"]), 1)
        self.assertEqual(result["trades"][0]["asset"], assets[1].key)
        self.assertEqual(result["decisions"][0]["gates"]["G06"]["observed"], "EXPLICIT_FIXED_4R_BENCHMARK")

    def test_udiff_validates_venue_date_and_series(self):
        _, day, _ = fixture()
        row = dict(zip(bhavcopy.UDIFF, [""] * len(bhavcopy.UDIFF)))
        row.update(TradDt=str(day), BizDt=str(day), Sgmt="CM", Src="NSE", FinInstrmTp="STK", FinInstrmId="1",
                   ISIN="IN0000000001", TckrSymb="DEMO", SctySrs="EQ", OpnPric="100", HghPric="105",
                   LwPric="95", ClsPric="101", TtlTradgVol="123")

        def parse(values):
            raw = (",".join(bhavcopy.UDIFF) + "\n" + ",".join(values[key] for key in bhavcopy.UDIFF)).encode()
            return bhavcopy.read(raw, day, today=day)

        self.assertEqual(parse(row)[1]["DEMO"].close, Decimal(101))
        for change in ({"Src": "BSE"}, {"TradDt": "2024-01-03"}, {"FinInstrmId": "invalid"}, {"LwPric": "150"}):
            with self.assertRaises(ValueError):
                parse({**row, **change})
