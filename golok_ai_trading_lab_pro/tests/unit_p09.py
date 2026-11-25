import unittest
from dataclasses import replace
from datetime import date, timedelta
from decimal import Decimal

from scripts.reproduce_p05 import fixture
from services import fixture_execution, performance, simulation, walk_forward


class PerformanceTests(unittest.TestCase):
    def test_daily_curve_uses_opening_and_recovers_after_drawdown(self):
        result = {"initial_cash": "100", "ending_cash": "120", "days": [
            {"date": "2024-01-02", "cash": "90"}, {"date": "2024-01-03", "cash": "120"},
        ]}
        points = performance.daily_curve(result)
        self.assertEqual([point["drawdown_percent"] for point in points], ["10", "0"])
        with self.assertRaises(ValueError):
            performance.daily_curve({**result, "ending_cash": "121"})
        with self.assertRaises(ValueError):
            performance.daily_curve({**result, "days": list(reversed(result["days"]))})

    def test_fixture_execution_uses_conservative_limits_and_ambiguous_stops(self):
        series, day, _costs = fixture()
        asset = series[0]
        cutoff = asset.sessions[day].exit_cutoff
        bar = asset.bars[5]
        self.assertIsNone(fixture_execution.entry_price(bar, Decimal("101"), Decimal("99"), 10))
        self.assertIsNone(fixture_execution.entry_price(bar, Decimal("102"), Decimal("99"), 11))
        self.assertEqual(fixture_execution.entry_price(bar, Decimal("102"), Decimal("99"), 10), Decimal("102"))
        self.assertEqual(fixture_execution.exit_result(bar, Decimal("99"), Decimal("114"), cutoff),
                         (Decimal("99"), "STOP_FIRST"))
        gap = replace(bar, open=Decimal("95"), low=Decimal("94"))
        self.assertEqual(fixture_execution.exit_result(gap, Decimal("99"), Decimal("114"), cutoff),
                         (Decimal("95"), "GAP_STOP"))
        target = replace(bar, low=Decimal("100"))
        self.assertEqual(fixture_execution.exit_result(target, Decimal("99"), Decimal("114"), cutoff),
                         (Decimal("114"), "TARGET"))

    def test_net_expectancy_counts_breakevens_and_costs_once(self):
        trades = [
            {"gross": gross, "fees": "2", "net": net, "quantity": 1, "entry": "100", "exit": price,
             "exit_time": timestamp, "loss": "5"}
            for gross, net, price, timestamp in (("12", "10", "112", "1"), ("-3", "-5", "97", "2"), ("2", "0", "102", "3"))
        ]
        result = {"initial_cash": "100", "ending_cash": "105", "gross": "11", "fees": "6", "net": "5",
                  "trades": trades, "days": [{"date": "A", "cash": "105"}]}
        report = performance.summarize(result)
        self.assertEqual(report["expectancy"], Decimal(5) / 3)
        self.assertEqual((report["wins"], report["losses"], report["breakevens"]), (1, 1, 1))
        self.assertEqual(report["closed_trade_cash_drawdown"]["amount"], Decimal(5))
        self.assertEqual(report["end_of_day_equity_drawdown"]["amount"], Decimal(0))
        self.assertIsNone(report["intraday_mark_to_market_drawdown"])
        with self.assertRaises(ValueError):
            performance.summarize({**result, "fees": "7"})

    def test_zero_trades_remain_insufficient(self):
        report = performance.summarize({"initial_cash": "100", "ending_cash": "100", "gross": "0",
                                        "fees": "0", "net": "0", "trades": [], "days": []})
        self.assertEqual(report["status"], "INSUFFICIENT_TRADES")
        self.assertIsNone(report["expectancy"])
        self.assertIsNone(report["win_rate"])
        self.assertIsNone(report["closed_trade_cash_drawdown"])

    def test_nse_cash_reference_reconciles_provisional_per_fill_estimate(self):
        day = date(2026, 3, 1)
        rules = []
        for side in ("buy", "sell"):
            amounts = {
                "brokerage": (".0003", "turnover"), "exchange": (".0000307", "turnover"),
                "sebi": (".000001", "turnover"), "gst": (".18", "tax_base"),
                "stamp": (".00003" if side == "buy" else "0", "turnover"),
                "stt": (".00025" if side == "sell" else "0", "turnover"),
                "spread": ("0", "fixed"), "slippage": ("0", "fixed"),
            }
            for charge, (rate, basis) in amounts.items():
                rules.append(simulation.Tariff(charge, day, None, "NSE", "equity_intraday", side, basis,
                                                Decimal(rate), "Provisional source comparison",
                                                maximum=Decimal(20) if charge == "brokerage" else None))
        schedule = simulation.CostSchedule(rules)
        buy = schedule.fees(day, "NSE", "buy", Decimal(100), 1000)
        sell = schedule.fees(day, "NSE", "sell", Decimal(105), 1000)
        self.assertEqual(sum(buy.values()), Decimal("30.34"))
        self.assertEqual(sum(sell.values()), Decimal("53.78"))
        self.assertEqual(Decimal(5000) - sum(buy.values()) - sum(sell.values()), Decimal("4915.88"))
        self.assertEqual(buy["gst"], Decimal("4.17"))
        self.assertEqual(sell["stt"], Decimal("26.25"))
        self.assertEqual(sum(schedule.fees(day, "NSE", "buy", Decimal(100), 1000, embedded_friction=True).values()),
                         Decimal("30.34"))
        with self.assertRaises(ValueError):
            schedule.fees(date(2026, 2, 28), "NSE", "buy", Decimal(100), 1000)

    def test_walk_forward_uses_disjoint_trading_windows_and_embargo(self):
        days = [date(2024, 1, 2) + timedelta(days=value) for value in (0, 1, 3, 4, 5, 8, 9, 10)]
        options = {"training": 2, "validation": 1, "evaluation": 1, "embargo": 1}
        rolling = list(walk_forward.folds(days, **options, expanding=False))
        expanding = list(walk_forward.folds(days, **options, expanding=True))
        self.assertEqual(len(rolling), 3)
        self.assertEqual(rolling[0], {"training": days[:2], "validation": days[3:4], "evaluation": days[5:6]})
        self.assertEqual(rolling[1]["training"], days[1:3])
        self.assertEqual(expanding[1]["training"], days[:3])
        self.assertEqual(expanding[-1]["evaluation"], days[-1:])
