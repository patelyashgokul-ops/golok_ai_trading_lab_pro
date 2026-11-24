import unittest
from datetime import date
from decimal import Decimal

from services import performance, simulation


class PerformanceTests(unittest.TestCase):
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
