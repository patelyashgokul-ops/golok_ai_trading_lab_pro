import json
import unittest
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from services import calendar, experiments, indicators, ingestion, market_data, simulation


class P04Tests(unittest.TestCase):
    def test_time_and_receipt_are_distinct(self):
        self.assertIsNone(ingestion.parse_feed_time("21-Jun-2023 10:46:10"))
        event = ingestion.parse_feed_time("2024-01-02T09:15:00+05:30")
        self.assertEqual(event.isoformat(), "2024-01-02T03:45:00+00:00")
        self.assertEqual(ingestion.quote_freshness(event, event + timedelta(seconds=31)), "stale")
        self.assertEqual(ingestion.quote_freshness(event, event - timedelta(seconds=1)), "unknown")

    def test_flat_zero_volume_indicator_reference(self):
        start = datetime(2024, 1, 2, tzinfo=timezone.utc)
        bars = [market_data.Candle(start + timedelta(minutes=i), *([Decimal(10)] * 4), 0)
                for i in range(40)]
        values = indicators.calculate(bars)
        expected = {
            "sma20": 10, "ema20": 10, "rsi14": 50, "macd": (0, 0, 0), "atr14": 0, "adx14": 0,
            "bollinger20": (10, 10, 10), "stochastic14": None, "relative_volume20": None, "roc10": 0,
            "obv": 0, "volatility20": 0, "high_low20": (10, 10), "opening_range15": None,
            "relative_strength": None, "gap": None, "volume_spike": None, "trend_slope20": 0, "vwap": None,
        }
        self.assertEqual({key: series[-1] for key, series in values.items()}, expected)

    def test_provider_normalization_rejects_future_close_and_wrong_stamp(self):
        day = date(2024, 1, 2)
        sessions = calendar.load_schedule(json.dumps([{"date": day.isoformat(), "kind": "regular",
            "open": "09:15", "close": "09:20", "entry_cutoff": "09:19", "exit_cutoff": "09:20"}]))
        session = sessions[day]
        row = (session.opening, Decimal(100), Decimal(101), Decimal(99), Decimal(100), 10)
        with self.assertRaisesRegex(ValueError, "complete open-stamped"):
            ingestion.normalize([row], session, 300, session.opening)
        with self.assertRaisesRegex(ValueError, "complete open-stamped"):
            ingestion.normalize([(session.closing, *row[1:])], session, 300, session.closing)
        received = session.closing + timedelta(microseconds=1)
        bar = ingestion.normalize([row], session, 300, received)[0]
        self.assertEqual(bar.available_at, session.closing + timedelta(seconds=1))

    def test_third_losing_session_is_suspended(self):
        fixture = Path(__file__).parent / "fixtures/p02"
        definition = json.loads((fixture / "spec.json").read_text())
        rows = (fixture / "candles.csv").read_bytes().splitlines()
        dates = ["2024-01-02", "2024-01-03", "2024-01-04"]
        raw = b"\n".join([rows[0], *(row.replace(b"2024-01-02", day.encode()) for day in dates for row in rows[1:])])
        bars = market_data.parse_csv(raw, as_of=datetime(2024, 2, 1, tzinfo=timezone.utc), temporal=True)
        sessions = calendar.load_schedule(json.dumps([{**definition["schedule"][0], "date": day} for day in dates]))
        outcome = experiments.simulate(bars, sessions, date(2024, 1, 2), date(2024, 1, 4), "NSE", 300,
                                       Decimal("0.05"), experiments.read_tariffs(json.dumps(definition["tariffs"])),
                                       "Synthetic suspension test", simulation.RiskPolicy())
        self.assertEqual(outcome["metrics"]["trades"], 2)
        self.assertEqual(outcome["days"][-1]["status"], "RISK_SUSPENDED")
        self.assertEqual((outcome["status"], outcome["requested_dates"], outcome["evaluated_dates"]),
                         ("risk_suspended", 3, 2))
