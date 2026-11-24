import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from services.market_data import Candle, check_series, parse_bar, parse_csv
from services.research import describe

AS_OF = datetime(2024, 1, 3, tzinfo=timezone.utc)
HEADER = b"close_time,open,high,low,close,volume\n"
LINE = b"2024-01-02T09:20:00+05:30,10,11,9,10,123\n"


class MarketDataTests(unittest.TestCase):
    def test_utc_normalization_and_exact_prices(self):
        bar = parse_csv(HEADER + LINE.replace(b",10,11", b",10.00000001,11"), as_of=AS_OF)[0]
        self.assertEqual(bar.close_time.isoformat(), "2024-01-02T03:50:00+00:00")
        self.assertEqual(bar.open, Decimal("10.00000001"))

    def test_invalid_prices_volume_and_timestamps(self):
        for old, new in [
            (b",11,", b",8,"), (b",9,", b",0,"), (b",10,", b",NaN,"),
            (b",123", b",-1"), (b",123", b",2147483648"), (b"+05:30", b""),
            (b"+05:30", b"+05:99"), (b"01-02", b"01-04"),
        ]:
            with self.subTest(new=new), self.assertRaises(ValueError):
                parse_csv(HEADER + LINE.replace(old, new), as_of=AS_OF)

    def test_duplicate_and_reversed_csv(self):
        for second in [LINE, LINE.replace(b"09:20", b"09:15")]:
            with self.assertRaisesRegex(ValueError, "strictly increasing"):
                parse_csv(HEADER + LINE + second, as_of=AS_OF)

    def test_empty_and_size_limits(self):
        with self.assertRaisesRegex(ValueError, "no candle"):
            parse_csv(HEADER, as_of=AS_OF)
        with self.assertRaisesRegex(ValueError, "512"):
            parse_csv(b"x" * 524289, as_of=AS_OF)

    def test_gap_count_and_date_boundary(self):
        bars = parse_csv(HEADER + LINE + LINE.replace(b"09:20", b"09:30"), as_of=AS_OF)
        self.assertEqual(check_series(bars, "5m"), 1)
        self.assertEqual(check_series(bars, "1d"), 0)


class ResearchTests(unittest.TestCase):
    def _bars(self):
        start = parse_bar("2024-01-02T09:20:00+05:30", "10", "11", "9", "10", "123", as_of=AS_OF).close_time
        return [
            Candle(start + timedelta(minutes=index * 5), Decimal(index + 10), Decimal(index + 11),
                   Decimal(index + 9), Decimal(index + 10), 300 if index == 20 else 100)
            for index in range(21)
        ]

    def test_reference_values_and_relative_volume_baseline(self):
        self.assertEqual(describe(self._bars()), {
            "sma20": Decimal("20.5"), "atr14": Decimal(2), "relative_volume20": Decimal(3),
        })

    def test_warmup_and_no_future_access(self):
        bars = self._bars()
        self.assertEqual(describe(bars[:14]), dict(sma20=None, atr14=None, relative_volume20=None))
        self.assertEqual(describe(bars[:20])["sma20"], Decimal("19.5"))
        self.assertIsNone(describe(bars[:20])["relative_volume20"])

    def test_atr_gaps_wilder_smoothing(self):
        bars = self._bars()[:15]
        last = Candle(bars[-1].close_time + timedelta(minutes=5), Decimal(38), Decimal(39),
                      Decimal(37), Decimal(38), 100)
        self.assertEqual(describe([*bars, last])["atr14"], Decimal(41) / 14)


if __name__ == "__main__":
    unittest.main()
