import io
import unittest
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from zipfile import ZipFile

from scripts.reproduce_p05 import fixture
from services import bhavcopy, price_integrity, providers, research_v3, strategies


class P06Tests(unittest.TestCase):
    day = date(2024, 1, 2)
    header = ",".join(bhavcopy.COLUMNS)
    row = "DEMO,EQ,10,12,9,11,11,10,100,1000,02-JAN-2024,4,IN0000000001"

    def parse(self, raw):
        return bhavcopy.read(raw, self.day, today=self.day)

    def test_csv_and_zip_match_and_invalid_members_fail(self):
        raw = (self.header + "\n" + self.row).encode()
        _, plain = self.parse(raw)
        self.assertEqual(plain["DEMO"].close, 11)
        for filename in ("report.csv", "../report.csv", "report.exe"):
            buffer = io.BytesIO()
            with ZipFile(buffer, "w") as archive:
                archive.writestr(filename, raw)
            if filename == "report.csv":
                self.assertEqual(self.parse(buffer.getvalue())[1], plain)
            else:
                with self.assertRaises(ValueError):
                    self.parse(buffer.getvalue())
        for invalid in (self.row + "\n" + self.row, self.row.replace(",12,", ",8,"),
                        self.row.replace("02-JAN", "03-JAN"), self.row.replace("DEMO", "=formula")):
            with self.assertRaises(ValueError):
                self.parse((self.header + "\n" + invalid).encode())

    def test_provider_caps_and_decisions(self):
        grants = {key: dict.fromkeys(providers.PERMISSIONS, True) for key in providers.SOURCES}
        self.assertIsNone(providers.route(providers.SOURCES, "live", ["live"], grants))
        self.assertIsNone(providers.route(["bhavcopy"], "daily", ["persist"], {}))
        self.assertIsNone(providers.route(["bhavcopy"], "daily", ["fit"], grants))
        self.assertEqual(providers.route(["yahoo", "bhavcopy"], "daily", ["persist"], grants), "bhavcopy")

    def test_equivalence_conflict_and_lineage(self):
        now = datetime.now(timezone.utc)
        a = price_integrity.Observation("fixture", "NSE", "INR", "1d", "raw", now, now, Decimal(100), "NSE")
        compare = lambda b: price_integrity.compare(a, b, now, Decimal(".05"))
        self.assertEqual(compare(a), "SHARED_UPSTREAM")
        self.assertEqual(compare(replace(a, upstream="unknown")), "UNKNOWN_LINEAGE")
        self.assertEqual(compare(replace(a, price=Decimal(101))), "CONFLICT")
        self.assertEqual(compare(replace(a, interval="5m")), "NON_EQUIVALENT")
        self.assertEqual(compare(replace(a, received_at=now + timedelta(seconds=1))), "UNVERIFIABLE")

    def test_strategy_triggers_and_anomaly(self):
        series, _, _ = fixture()
        base = series[0].bars[0]
        rising = [replace(base, close=Decimal(100+i), low=Decimal(97+i), high=Decimal(101+i)) for i in range(16)]
        self.assertEqual(strategies.trend_following(rising, None), None)
        rising[-1] = replace(rising[-1], close=Decimal(116))
        self.assertEqual(strategies.trend_following(rising, None), Decimal(109))
        bars = [base] * 20 + [replace(base, volume=base.volume*4, close=base.high+1, high=base.high+2)]
        self.assertEqual(strategies.volume_breakout(bars, None), base.low)
        self.assertTrue(research_v3.analyze(bars)["RE-20"]["finding"]["volume_expansion"])
