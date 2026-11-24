import json
import unittest
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

from services import calendar, experiments, market_data, paper, research_v3, simulation

FIXTURES = Path(__file__).parent / "fixtures/p02"
DAY = date(2024, 1, 2)
AS_OF = datetime(2024, 2, 1, tzinfo=timezone.utc)


class P03Tests(unittest.TestCase):
    def test_split_calendar_has_no_cross_segment_bars(self):
        data = [{"date": DAY.isoformat(), "kind": "special", "open": "09:15", "close": "11:30",
                 "entry_cutoff": "11:10", "exit_cutoff": "11:25",
                 "segments": [["09:15", "09:28"], ["11:00", "11:30"]]}]
        session = calendar.load_schedule(json.dumps(data))[DAY]
        slots = session.slots(300)
        self.assertEqual(len(slots), 9)
        self.assertEqual((slots[2][1] - slots[2][0]).total_seconds(), 180)
        self.assertEqual(session.slots(None), [])
        opening, closing = slots[2][0], slots[3][1]
        bar = market_data.Candle(closing, Decimal(1), Decimal(1), Decimal(1), Decimal(1), 1, opening, closing)
        with self.assertRaisesRegex(ValueError, "outside"):
            calendar.validate_bar(bar, {DAY: session}, 300)

    def test_multiple_sessions_stop_at_unknown_calendar_and_reconcile_trades(self):
        spec = json.loads((FIXTURES / "spec.json").read_text())
        bars = market_data.parse_csv((FIXTURES / "candles.csv").read_bytes(), as_of=AS_OF, temporal=True)
        result = experiments.simulate(
            bars, calendar.load_schedule(json.dumps(spec["schedule"])), DAY, date(2024, 1, 3),
            "NSE", 300, Decimal("0.05"), experiments.read_tariffs(json.dumps(spec["tariffs"])), "Synthetic",
            simulation.RiskPolicy(),
        )
        self.assertEqual(result["status"], "unresolved")
        self.assertEqual(result["days"][-1]["status"], "UNRESOLVED")
        self.assertEqual(result["metrics"]["trades"], 1)
        trade = result["trades"][0]
        ending, events = paper.postings([trade], 5_000_000)
        available, reserved, position = 5_000_000, 0, 0
        for event in events:
            available += event["cash_delta"]
            reserved += event["reserved_delta"]
            position += event["quantity_delta"]
            self.assertGreaterEqual(min(available, reserved, position), 0)
            self.assertEqual((available, reserved), (event["available_after"], event["reserved_after"]))
        self.assertEqual((available, reserved, position), (ending, 0, 0))
        self.assertEqual(ending - 5_000_000, paper.paise(trade["net"]))
        with self.assertRaises(ValueError):
            paper.postings([trade], 5)
        with self.assertRaises(ValueError):
            paper.paise("1.001")

    def test_supplemental_algorithms_warmup_and_preceding_levels(self):
        from dataclasses import replace
        bars = market_data.parse_csv((FIXTURES / "candles.csv").read_bytes(), as_of=AS_OF, temporal=True)
        observed = research_v3.analyze(bars)
        self.assertEqual(observed["RE-03"]["status"], "COMPLETED")
        self.assertEqual(observed["RE-04"]["finding"]["shape"], "doji")
        self.assertEqual(observed["RE-06"]["status"], "INSUFFICIENT_DATA")
        prior = [bars[0]] * 20
        current = replace(bars[-1], high=Decimal("100000"), close=Decimal("1000"))
        results = research_v3.analyze([*prior, current])
        self.assertEqual(results["RE-06"]["finding"]["rolling_resistance"], "101")
        self.assertEqual(results["RE-19"]["finding"]["up_closes"], 1)
        self.assertTrue(all(row["finding"] is None for row in research_v3.analyze(bars, True).values()))
