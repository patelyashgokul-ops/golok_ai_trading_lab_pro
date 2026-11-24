import json
import unittest
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal as D
from unittest.mock import patch

from services import backtest, calendar, indicators, market_data, simulation, smartapi

DAY = date(2024, 1, 2)
NOW = datetime(2024, 2, 1, tzinfo=timezone.utc)


def session_schedule():
    return calendar.load_schedule(json.dumps([
        {"date": "2024-01-02", "kind": "regular", "open": "09:15", "close": "10:00",
         "entry_cutoff": "09:45", "exit_cutoff": "10:00", "pre_open": "09:00"},
        {"date": "2024-01-03", "kind": "closed"},
        {"date": "2024-01-04", "kind": "special", "open": "18:00", "close": "19:00",
         "entry_cutoff": "18:45", "exit_cutoff": "18:55"},
    ]))


def costs():
    return simulation.CostSchedule([
        simulation.Tariff(name, DAY, None, "NSE", "equity_intraday", side,
                          "tax_base" if name == "gst" else "fixed",
                          D("1.005") if name == "brokerage" else D(0), "Hypothetical test values")
        for name in sorted(simulation.CHARGES) for side in ("buy", "sell")
    ])


def bars_for(session):
    return [
        market_data.Candle(end, D("100"), D("101"), D("99"), D("100"), 1000, start, end)
        for start, end in session.slots(300)
    ]


class CalendarTests(unittest.TestCase):
    def test_calendar_and_time_availability(self):
        schedule = session_schedule()
        day = schedule[DAY]
        bars = bars_for(day)
        self.assertEqual(day.opening.hour, 3)
        self.assertEqual(day.opening.minute, 45)
        self.assertEqual(len(day.slots(None)), 1)
        self.assertEqual(day.slots(1800)[1][1], day.closing)
        self.assertEqual(calendar.missing_observations(bars[:1] + bars[2:4], schedule, 300), 1)
        special = schedule[date(2024, 1, 4)]
        self.assertEqual(calendar.missing_observations([bars[-1], bars_for(special)[0]], schedule, 300), 0)
        with self.assertRaisesRegex(ValueError, "No eligible"):
            calendar.validate_bar(replace(bars[0], close_time=bars[0].close_time + timedelta(days=1)), schedule, 300)
        with self.assertRaisesRegex(ValueError, "incomplete"):
            calendar.missing_observations([bars[-1], bars_for(special)[0]], {DAY: day, special.day: special}, 300)
        with self.assertRaisesRegex(ValueError, "outside"):
            calendar.validate_bar(replace(bars[0], open_time=bars[0].open_time - timedelta(minutes=1)), schedule, 300)

    def test_temporal_csv_rejects_early_availability_and_future(self):
        header = (",".join(market_data.TEMPORAL_COLUMNS) + "\n").encode()
        data = b"2024-01-02T09:20:00+05:30,100,102,99,101,100,2024-01-02T09:15:00+05:30,2024-01-02T09:21:00+05:30"
        self.assertEqual(market_data.parse_csv(header + data, as_of=NOW, temporal=True)[0].available_at.minute, 51)
        for invalid in (data.replace(b"09:21", b"09:19"), data.replace(b"01-02T09:21", b"02-02T09:21")):
            with self.assertRaises(ValueError):
                market_data.parse_csv(header + invalid, as_of=NOW, temporal=True)


class IndicatorsTests(unittest.TestCase):
    def test_reference_values_and_all_prefixes(self):
        start = datetime(2024, 1, 1, tzinfo=timezone.utc)
        bars = [
            market_data.Candle(start + timedelta(minutes=i), D(100+i), D(101+i), D(99+i), D(100+i), 100)
            for i in range(40)
        ]
        series = indicators.calculate(bars)
        self.assertEqual(len(series), 19)
        self.assertEqual(series["sma20"][19], D("109.5"))
        self.assertEqual(series["ema20"][19], D("109.5"))
        self.assertEqual(series["rsi14"][14], 100)
        self.assertEqual(series["atr14"][14], 2)
        self.assertEqual(series["adx14"][27], 100)
        self.assertEqual(series["macd"][25], (D(7), None, None))
        self.assertEqual(series["macd"][33], (D(7), D(7), D(0)))
        self.assertEqual(series["relative_volume20"][20], 1)
        self.assertEqual(series["trend_slope20"][19], 1)
        self.assertEqual(series["obv"][20], 2000)
        self.assertEqual(series["high_low20"][19], (D(120), D(99)))
        self.assertEqual(series["roc10"][10], D("0.1"))
        self.assertEqual(series["bollinger20"][19][1], D("109.5"))
        self.assertEqual(series["stochastic14"][13], D(1400) / 15)
        self.assertIsNone(series["relative_strength"][-1])
        for cutoff in (1, 14, 20, 26, 35):
            self.assertEqual(indicators.calculate(bars[:cutoff]), {key: values[:cutoff] for key, values in series.items()})

    def test_session_reset_and_opening_range(self):
        schedule = session_schedule()
        bars = bars_for(schedule[DAY])
        special = schedule[date(2024, 1, 4)]
        another = replace(bars_for(special)[0], open=D(120), close=D(120), high=D(121), low=D(119))
        series = indicators.calculate(bars + [another], sessions=schedule)
        self.assertEqual(series["opening_range15"][:3], [None, None, (D(101), D(99))])
        self.assertEqual(series["vwap"][0], 100)
        self.assertEqual(series["vwap"][-1], 120)
        self.assertEqual(series["gap"][-1], D("0.2"))
        self.assertIsNone(indicators.calculate(bars[1:], sessions=schedule)["vwap"][0])


class SimulationTests(unittest.TestCase):
    def test_tariffs_effective_date_and_risk(self):
        schedule = costs()
        self.assertEqual(schedule.fees(DAY, "NSE", "buy", D(100), 1)["brokerage"], D("1.01"))
        self.assertNotIn("spread", schedule.fees(DAY, "NSE", "buy", D(100), 1, embedded_friction=True))
        with self.assertRaisesRegex(ValueError, "missing"):
            schedule.fees(DAY - timedelta(days=1), "NSE", "buy", D(100), 1)
        with self.assertRaises(ValueError):
            schedule.fees(DAY, "NSE", "buy", D(100), 0)
        outcome = simulation.size_long(D(100), D(98), D(108), D(".05"), 1000, DAY, "NSE", schedule)
        self.assertEqual(outcome.quantity, 10)
        self.assertEqual(outcome.loss, D("22.52"))
        self.assertEqual(simulation.size_long(D(100), D(98), D(101), D(".05"), 1000, DAY, "NSE", schedule).quantity, 0)

    def test_breakout_reproducibility_and_stop_first(self):
        session = session_schedule()[DAY]
        bars = bars_for(session)
        bars[3] = replace(bars[3], close=D(102), high=D(103), volume=2000)
        bars[5] = replace(bars[5], open=D(102), close=D(101), high=D(120), low=D(98))
        def run(values, origin="synthetic"):
            return backtest.replay(values, session, "NSE", 300, D(".05"), costs(),
                                   source="Fixture", partition="holdout", origin=origin)
        result = run(bars)
        self.assertEqual(result, run(bars))
        self.assertEqual(result["trade"]["entry_time"], bars[5].open_time)
        self.assertEqual(result["trade"]["exit_reason"], "STOP_AMBIGUITY")
        self.assertLess(result["trade"]["net"], result["trade"]["gross"])
        self.assertEqual(result["status"], "SYNTHETIC_CORRECTNESS_ONLY")
        with self.assertRaises(ValueError):
            run(bars, "imported")
        with self.assertRaisesRegex(ValueError, "complete"):
            run(bars[:2] + bars[3:])


class ProviderTests(unittest.TestCase):
    def test_disabled_transport_and_endpoint_scope(self):
        with patch.dict("os.environ", {}, clear=True):
            client = smartapi.SmartAPI.from_environment()
        self.assertEqual(client.state, "NOT_CONFIGURED")
        with self.assertRaisesRegex(smartapi.ProviderError, "NOT_CONFIGURED"):
            client.authenticate("fixture", "fixture", "fixture")
        self.assertEqual(smartapi.CAPABILITIES, {"authenticate", "history", "quote"})
        with self.assertRaisesRegex(smartapi.ProviderError, "Unsupported"):
            smartapi._https("unsupported", {}, {}, 7)

    def test_fixture_auth_history_quote_and_rate_limit(self):
        time = [10]
        calls = []
        responses = iter([
            {"status": True, "data": {"jwtToken": "session.fixture"}},
            {"status": True, "data": [["2024-01-02T09:20:00+05:30", 100, 101, 99, 100, 123]]},
            {"status": True, "data": {"fetched": [{"exchange": "NSE", "symbolToken": "123", "ltp": "100.10"}]}},
            {"status": False, "errorcode": "AG8001", "message": "session.fixture"},
        ])
        def send(operation, headers, payload, timeout):
            calls.append(operation)
            self.assertEqual(timeout, 7)
            return next(responses)
        client = smartapi.SmartAPI(send, clock=lambda: time[0])
        client.authenticate("fixture", "fixture", "fixture")
        with self.assertRaisesRegex(smartapi.ProviderError, "^RATE_LIMITED$"):
            client.quote("NSE", "123")
        time[0] += 5
        start = datetime(2024, 1, 2, 3, 45, tzinfo=timezone.utc)
        rows = client.history("NSE", "123", "5m", start, start + timedelta(minutes=5))
        self.assertEqual(rows[0][-1], 123)
        time[0] += 5
        self.assertEqual(client.quote("NSE", "123")["freshness"], "unknown")
        time[0] += 5
        with self.assertRaisesRegex(smartapi.ProviderError, "^AUTH_REQUIRED$"):
            client.quote("NSE", "123")
        self.assertEqual(calls, ["authenticate", "history", "quote", "quote"])

    def test_timeout_sanitizes_transport_error(self):
        def fail(*_):
            raise TimeoutError("fixture-sensitive-payload")
        client = smartapi.SmartAPI(fail)
        with self.assertRaisesRegex(smartapi.ProviderError, "^DISCONNECTED$"):
            client.authenticate("fixture", "fixture", "fixture")
