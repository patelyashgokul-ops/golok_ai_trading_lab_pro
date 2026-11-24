import json
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

from odoo.exceptions import AccessError, ValidationError
from odoo.tests import TransactionCase, new_test_user, tagged
from odoo.tools.binary import BinaryBytes

MODULE = "golok_ai_trading_lab_pro"


@tagged("at_install", "-post_install")
class TestLab(TransactionCase):
    def test_p08_authorized_replay_requires_verified_publication_and_current_rights(self):
        files = Path(__file__).parent / "fixtures/p02"
        spec = json.loads((files / "spec.json").read_text())
        reference = "https://example.test/fixture-publication"
        review = self.env["golok.lab.source.review"].with_user(self.admin).create({
            "provider": "manual", "upstream": "Authored market-contract test",
            "terms_url": "https://example.test/fixture-terms", "documentation": reference,
            "evidence": "Generated test grant", "purpose": "Contract testing",
            "restrictions": "Synthetic input only", "expires": "2099-01-01", "storage_policy": "archive",
            "query": True, "display": True, "persist": True, "backtest": True, "raw_share_ohlcv": True,
        })
        calendar = self.env["golok.lab.calendar"].with_user(self.admin).create({
            "name": "Contract market calendar", "exchange": "NSE",
            "verification": "reviewed", "source": "https://www.nseindia.com/market-data",
            "verified_on": "2024-01-01", "schedule": json.dumps(spec["schedule"]),
        })
        mapping = self.env["golok.lab.mapping"].with_user(self.admin).create({
            "instrument_id": self.instrument.id, "symbol": self.instrument.symbol, "provider": "manual",
            "token": "991", "starts": "2024-01-01", "tick": "0.05", "listing_status": "listed",
            "source": reference, "revision": "authored-1", "verification": "reviewed", "isin": "IN0000000001",
        })
        dataset = self.env["golok.lab.dataset"].with_user(self.analyst).create({
            "name": "Authored historical contract", "source": review.upstream,
            "origin": "imported", "interval": "5m", "instrument_id": self.instrument.id,
            "calendar_id": calendar.id, "mapping_id": mapping.id,
        })
        data = (files / "candles.csv").read_bytes()
        values = {"dataset_id": dataset.id, "upload": BinaryBytes(data)}
        importer = self.env["golok.lab.import"]
        importer.with_user(self.analyst).create(values).action_import()
        tariff = self.env["golok.lab.tariff"].with_user(self.admin).create({
            "name": "Historical contract costs", "lines": json.dumps(spec["tariffs"]),
        })
        wizard = self.env["golok.lab.portfolio.wizard"].with_user(self.analyst).create({
            "dataset_ids": [(6, 0, dataset.ids)], "tariff_id": tariff.id, "starts": spec["date"],
            "ends": spec["date"], "strategy": "ST-01", "target_policy": "fixed_4r",
        })
        with self.assertRaises(AccessError):
            wizard.action_run_authorized_history()
        with self.assertRaises(AccessError):
            importer.with_user(self.analyst).create(values).action_attest_publication()
        verifier = importer.with_user(self.admin)
        altered = data.replace(b",1000,", b",1001,", 1)
        bad = verifier.create({**values, "publication_evidence": reference, "upload": BinaryBytes(altered)})
        with self.assertRaises(ValidationError):
            bad.action_attest_publication()
        proof = verifier.create({**values, "publication_evidence": reference})
        proof.action_attest_publication()
        proof.action_attest_publication()
        with self.assertRaises(AccessError):
            importer.with_user(self.analyst).create(values).action_import()
        with self.assertRaises(ValidationError):
            wizard.action_run()
        action = wizard.action_run_authorized_history()
        result = self.env[action["res_model"]].with_user(self.analyst).browse(action["res_id"])
        self.assertEqual(result.id, wizard.action_run_authorized_history()["res_id"])
        self.assertEqual(json.loads(result.result)["scope"], "AUTHORIZED_HISTORICAL_SIMULATION")
        self.assertEqual(json.loads(result.specification)["inputs"][0]["verified_dataset_digest"],
                         dataset.replay_publication_digest)
        with self.assertRaises(AccessError):
            result._export_rows([["result"]], _is_toplevel_call=False)
        review.action_revoke()
        self.assertFalse(result.search([("id", "=", result.id)]))
        with self.assertRaises(AccessError):
            result.read(["result"])
        with self.assertRaises(AccessError):
            wizard.action_run_authorized_history()

    def test_p08_generated_fixture_lineage_is_immutable_and_idempotent(self):
        from ..models.lab import _input_digest
        from ..services import fixture_generator

        spec = json.loads((Path(__file__).parent / "fixtures/p02/spec.json").read_text())
        revision = self.env["golok.lab.calendar"].with_user(self.admin).create({
            "name": "Generated fixture", "source": "Authored regression", "exchange": "NSE", "verification": "fixture",
            "verified_on": "2024-01-01", "schedule": json.dumps(spec["schedule"])})
        with self.assertRaises(AccessError):
            revision.with_user(self.analyst).action_generate_fixture()
        action = revision.action_generate_fixture()
        self.assertEqual(revision.action_generate_fixture()["res_id"], action["res_id"])
        dataset = self.env["golok.lab.dataset"].with_user(self.analyst).browse(action["res_id"])
        self.assertTrue(dataset.instrument_id.symbol.startswith("SYN-P08-"))
        self.assertEqual(dataset.lineage_status, "generated_fixture")
        self.assertEqual((dataset.fixture_version, dataset.fixture_seed), (fixture_generator.VERSION, fixture_generator.SEED))
        rows = self.env["golok.lab.candle"].with_user(self.analyst).search(
            [("dataset_id", "=", dataset.id)], order="close_time")
        self.assertEqual(dataset.fixture_digest, _input_digest([row._to_bar() for row in rows], revision))
        self.assertEqual([row._to_bar() for row in rows], fixture_generator.generate(revision._sessions()))
        with self.assertRaises(AccessError):
            dataset._import_bars([rows[0]._to_bar()])
        with self.assertRaises(AccessError):
            self.env["golok.lab.dataset"].with_user(self.analyst).create({
                "name": "Forged", "source": "Forged", "origin": "synthetic", "interval": "5m",
                "instrument_id": self.instrument.id, "fixture_version": fixture_generator.VERSION})
        tariff = self.env["golok.lab.tariff"].with_user(self.admin).create({
            "name": "Timing contract fixture", "lines": json.dumps(spec["tariffs"])})
        wizard = self.env["golok.lab.portfolio.wizard"].with_user(self.analyst).create({
            "dataset_ids": [(6, 0, dataset.ids)], "tariff_id": tariff.id, "starts": spec["date"], "ends": spec["date"],
            "strategy": "ST-01"})
        action = wizard.action_run_timing_fixture()
        self.assertEqual(action["res_id"], wizard.action_run_timing_fixture()["res_id"])
        replay = self.env[action["res_model"]].with_user(self.analyst).browse(action["res_id"])
        self.assertTrue(replay.contract_fixture)
        self.assertEqual(json.loads(replay.result)["scope"], "HISTORICAL_CONTRACT_FIXTURE_ONLY")
        self.assertEqual(json.loads(replay.specification)["inputs"][0]["generated_fixture_digest"], dataset.fixture_digest)
        wizard.dataset_ids = self.dataset
        with self.assertRaises((AccessError, ValidationError)):
            wizard.action_run_timing_fixture()

    def test_p07_manual_market_csv_requires_active_company_grant(self):
        analyst = self.env["golok.lab.dataset"].with_user(self.analyst)
        dataset_values = {"name": "External source fixture", "source": "Licensed source test",
                          "instrument_id": self.instrument.id, "interval": "5m", "origin": "imported"}
        with self.assertRaises(AccessError):
            analyst.create(dataset_values)
        with self.assertRaises(AccessError):
            analyst.with_context(default_origin="imported").create(
                {key: value for key, value in dataset_values.items() if key != "origin"})
        values = {"provider": "manual", "terms_url": "https://example.test/terms",
                  "documentation": "https://example.test/schema", "evidence": "Generated test grant",
                  "purpose": "Internal descriptive analysis", "restrictions": "Local use",
                  "expires": "2099-01-01", "query": True, "display": True, "persist": True, "storage_policy": "archive",
                  "research": True, "upstream": "Licensed source test"}
        reviews = self.env["golok.lab.source.review"].with_user(self.admin)
        reviews.create(values)
        with self.assertRaises(AccessError):
            analyst.create({**dataset_values, "source": "Different publisher"})
        data = analyst.create(dataset_values)
        self.assertEqual(data.lineage_status, "active")
        for purpose in ("historical_replay", "optimization", "fitting", "automatic_sync", "prospective_paper",
                        "live", "export", "redistribution", "unknown"):
            with self.subTest(purpose=purpose), self.assertRaises(AccessError):
                data._permit(purpose)
        self._wizard(self._lines(1), data).action_import()
        candles = self.env["golok.lab.candle"].with_user(self.analyst)
        candle = candles.search([("dataset_id", "=", data.id)])
        self.assertEqual(len(candle), 1)
        self.analyst.sudo().write({"group_ids": [(4, self.env.ref("base.group_allow_export").id)]})
        with self.assertRaises(AccessError):
            candle.export_data(["close_price"])
        runs = self.env["golok.lab.run"].with_user(self.analyst)
        run = runs.create({"dataset_id": data.id, "as_of": self.start})
        jobs = self.env["golok.lab.research.job"]
        job = jobs.with_user(self.analyst).create({"dataset_id": data.id, "cutoff": self.start})
        expired = reviews.create({**values, "expires": "2000-01-01"})
        with self.assertRaises(AccessError):
            self._wizard(self._lines(2), data).action_import()
        with self.assertRaises(AccessError):
            runs.create({"dataset_id": data.id, "as_of": self.start})
        with self.assertRaises(AccessError):
            run.read(["evidence"])
        self.assertFalse(candles.search([("dataset_id", "=", data.id)]))
        jobs._cron_run_next()
        self.assertEqual(job.state, "blocked")
        expired.action_revoke()
        self.assertTrue(expired.revoked_at)

    def test_p08_revocation_retention_and_nested_exports(self):
        from unittest.mock import patch
        from odoo import fields

        today = fields.Date.today()
        until = today + timedelta(days=1)
        reviews = self.env["golok.lab.source.review"].with_user(self.admin)
        grants = {
            "provider": "manual", "terms_url": "https://example.test/terms",
            "documentation": "https://example.test/schema", "evidence": "Authored permission fixture",
            "purpose": "Descriptive research", "restrictions": "Local testing only",
            "expires": today + timedelta(days=30), "query": True, "display": True, "persist": True, "research": True,
        }
        analyst = self.env["golok.lab.dataset"].with_user(self.analyst)
        runs = self.env["golok.lab.run"].with_user(self.analyst)
        candles = self.env["golok.lab.candle"].with_user(self.analyst)
        fixed = reviews.create({**grants, "upstream": "Fixed rights", "storage_policy": "fixed", "retain_until": until})
        revocable = reviews.create({**grants, "upstream": "Revocable rights", "storage_policy": "archive"})
        datasets, snapshots = [], []
        for grant in (fixed, revocable):
            source = analyst.create({"name": grant.upstream, "source": grant.upstream, "origin": "imported",
                                     "instrument_id": self.instrument.id, "interval": "5m"})
            self._wizard(self._lines(1), source).action_import()
            dataset_domain = [("dataset_id", "=", source.id)]
            self.assertEqual(candles.search_count(dataset_domain), 1)
            snapshot = runs.create({"dataset_id": source.id, "as_of": self.start})
            self.assertTrue(snapshot.read(["evidence"]))
            with self.assertRaises(AccessError):
                snapshot._export_rows([["evidence"]], _is_toplevel_call=False)
            datasets.append(source)
            snapshots.append(snapshot)
        revocable.action_revoke()
        self.assertEqual(datasets[1].sudo().lineage_status, "revoked")
        with self.assertRaises(AccessError):
            runs.create({"dataset_id": datasets[1].id, "as_of": self.start})
        with self.assertRaises(AccessError):
            snapshots[1].read(["evidence"])
        with patch.object(fields.Date, "today", return_value=until + timedelta(days=1)):
            self.env.invalidate_all()
            self.assertEqual(fixed.lifecycle, "retention_expired")
            self.assertFalse(candles.search([("dataset_id", "=", datasets[0].id)]))
            with self.assertRaises(AccessError):
                snapshots[0].read(["evidence"])
            with self.assertRaises(AccessError):
                self._wizard(self._lines(2), datasets[0]).action_import()
            self.assertTrue(candles.sudo().search([("dataset_id", "=", datasets[0].id)]))
        legacy = analyst.create({"name": "Legacy market data", "source": fixed.upstream,
                                 "origin": "imported", "instrument_id": self.instrument.id, "interval": "1m"})
        self._wizard(self._lines(1), legacy).action_import()
        legacy_candles = [("dataset_id", "=", legacy.id)]
        self.assertEqual(candles.search_count(legacy_candles), 1)
        self.env.flush_all()
        self.env.cr.execute("UPDATE golok_lab_dataset SET source_review_id=NULL, publication_basis=NULL WHERE id=%s",
                            (legacy.id,))
        legacy.invalidate_recordset()
        self.assertEqual(legacy.lineage_status, "insufficient")
        self.assertFalse(candles.search(legacy_candles))
        self.assertEqual(candles.sudo().search_count(legacy_candles), 1)
        with self.assertRaises(AccessError):
            legacy._permit("research")
        transient = reviews.create({**grants, "upstream": "Transient rights", "storage_policy": "transient"})
        self.assertEqual(transient.lifecycle, "transient")
        with self.assertRaises(AccessError):
            analyst.create({"name": transient.upstream, "source": transient.upstream, "origin": "imported",
                            "instrument_id": self.instrument.id, "interval": "5m"})

    def test_p06_review_and_daily_fixture(self):
        import base64
        from ..services.bhavcopy import COLUMNS, UDIFF

        reviews = self.env["golok.lab.source.review"].with_user(self.admin)
        imports = self.env["golok.lab.daily.import"].with_user(self.admin)
        calendar = self.env["golok.lab.calendar"].with_user(self.admin).create({
            "name": "Daily fixture", "source": "Synthetic", "exchange": "NSE", "verification": "fixture",
            "verified_on": "2024-01-01", "schedule": json.dumps([
                {"date": f"2024-01-0{day}", "kind": "regular", "open": "09:15",
                 "close": "15:30", "entry_cutoff": "14:30", "exit_cutoff": "15:20"} for day in (2, 3, 4)]),
        })
        payload = ",".join(COLUMNS) + "\nDEMO,EQ,10,12,9,11,11,10,100,1000,02-JAN-2024,4,IN0000000001"
        vals = {"source": "fixture", "day": "2024-01-02", "calendar_id": calendar.id,
                "upload": base64.b64encode(payload.encode()).decode()}
        with self.assertRaises(AccessError):
            imports.create(vals)
        grant = {"provider": "fixture", "terms_url": "fixture", "documentation": "fixture",
                 "evidence": "Self-authored OHLC", "purpose": "Software testing", "restrictions": "Synthetic only",
                 "expires": "2099-01-01", "display": True, "query": True, "persist": True, "storage_policy": "archive"}
        reviews.create(grant)
        accepted = imports.create(vals)
        self.assertEqual((accepted.status, accepted.count), ("accepted", 1))
        self.assertEqual(accepted, imports.create(vals))
        admin = self.env["golok.lab.instrument"].with_user(self.admin)
        instrument = admin.create({"name": "Daily fixture member", "symbol": "DEMO", "exchange": "NSE"})
        self.env["golok.lab.mapping"].with_user(self.admin).create({
            "instrument_id": instrument.id, "symbol": "DEMO", "provider": "manual", "token": "500",
            "starts": "2024-01-01", "tick": "0.05", "lot": 1, "listing_status": "listed",
            "source": "Authored fixture", "revision": "p08", "verification": "fixture", "isin": "IN0000000001",
        })
        accepted.action_normalize()
        dataset = accepted.normalized_dataset_ids
        self.assertEqual((len(dataset), dataset.interval), (1, "1d"))
        self.assertEqual(self.env["golok.lab.candle"].search_count([("dataset_id", "=", dataset.id)]), 1)
        cutoff = self.env["golok.lab.candle"].search([("dataset_id", "=", dataset.id)]).available_at
        from unittest.mock import patch
        from odoo import fields
        with patch.object(fields.Datetime, "now", return_value=cutoff):
            result = self.env["golok.lab.run"].with_user(self.analyst).create({"dataset_id": dataset.id, "as_of": cutoff})
        self.assertEqual(result.bar_count, 1)
        accepted.action_normalize()
        self.assertEqual(accepted.normalized_dataset_ids, dataset)

        modern = {name: "" for name in UDIFF}
        modern.update(TradDt="2024-01-04", BizDt="2024-01-04", Sgmt="CM", Src="NSE", FinInstrmTp="STK",
                      FinInstrmId="500", ISIN="IN0000000001", TckrSymb="DEMO", SctySrs="EQ",
                      OpnPric="10", HghPric="12", LwPric="9", ClsPric="11", TtlTradgVol="100")
        later = ",".join(UDIFF) + "\n" + ",".join(modern[name] for name in UDIFF)
        modern_batch = imports.create({**vals, "day": "2024-01-04", "upload": base64.b64encode(later.encode()).decode()})
        modern_batch.action_normalize()
        self.assertEqual(modern_batch.normalized_dataset_ids, dataset)

        runs = self.env["golok.lab.run"].with_user(self.analyst)

        def latest_daily_result():
            latest_receipt = self.env["golok.lab.candle"].search(
                [("dataset_id", "=", dataset.id)], order="available_at desc", limit=1).available_at
            with patch.object(fields.Datetime, "now", return_value=latest_receipt):
                return runs.create({"dataset_id": dataset.id, "as_of": latest_receipt})

        gap = latest_daily_result()
        self.assertEqual((gap.bar_count, gap.gap_count), (2, 1))
        middle = imports.create({**vals, "day": "2024-01-03",
                                 "upload": base64.b64encode(payload.replace("02-JAN", "03-JAN").encode()).decode()})
        middle.action_normalize()
        self.assertEqual(middle.normalized_dataset_ids, dataset)
        filled = latest_daily_result()
        self.assertEqual((filled.bar_count, filled.gap_count), (3, 0))
        self.assertEqual(gap.gap_count, 1)
        correction_payload = {**vals, "upload": base64.b64encode(
            payload.replace(",100,1000,", ",101,1000,").encode()).decode()}
        self.assertEqual(imports.create(correction_payload).status, "quarantine")
        correction_request = {**correction_payload, "corrects_id": accepted.id,
                              "correction_evidence": "Authored publisher correction fixture"}
        with self.assertRaises(ValidationError):
            imports.create({**correction_request, "corrects_id": modern_batch.id})
        correction = imports.create(correction_request)
        self.assertEqual((correction.status, correction.corrects_id), ("accepted", accepted))
        self.assertEqual(correction, imports.create(correction_request))
        self.assertEqual(accepted, imports.create({**vals, "corrects_id": accepted.id,
                                                  "correction_evidence": "Duplicate payload"}))
        correction.action_normalize()
        corrected = correction.normalized_dataset_ids
        correction.action_normalize()
        self.assertEqual(correction.normalized_dataset_ids, corrected)
        self.assertEqual(corrected.daily_revision_id, correction)
        self.assertEqual(len(corrected.daily_revision_digest), 64)
        candles = self.env["golok.lab.candle"]
        corrected_bar = candles.search([("dataset_id", "=", corrected.id)])
        original_bar = candles.search([("dataset_id", "=", dataset.id), ("close_time", "=", corrected_bar.close_time)])
        self.assertEqual((original_bar.volume, corrected_bar.volume), (100, 101))
        with self.assertRaises(AccessError):
            corrected._import_bars([corrected_bar._to_bar()])
        self.assertEqual((filled.bar_count, filled.gap_count), (3, 0))
        self.assertEqual(imports.create({**vals, "upload": "eA=="}).status, "quarantine")
        with self.assertRaises(AccessError):
            imports.with_user(self.viewer).create(vals)
        reviews.create({**grant, "persist": False})
        with self.assertRaises(AccessError):
            imports.create(vals)
        reviews.create({**grant, "expires": "2000-01-01"})
        with self.assertRaises(AccessError):
            imports.create(vals)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.other_company = cls.env["res.company"].create({"name": "Independent Research Company"})
        cls.admin = new_test_user(cls.env, login="lab-system", groups=f"{MODULE}.group_admin")
        cls.analyst = new_test_user(cls.env, login="lab-analyst", groups=f"{MODULE}.group_analyst")
        cls.viewer = new_test_user(cls.env, login="lab-viewer", groups=f"{MODULE}.group_viewer")
        cls.instrument = cls.env["golok.lab.instrument"].with_user(cls.admin).create({
            "name": "Fixture Equity", "symbol": "FIXTURE", "exchange": "NSE",
        })
        cls.dataset = cls.env["golok.lab.dataset"].with_user(cls.analyst).create({
            "name": "Synthetic CSV", "source": "Test fixture", "origin": "synthetic",
            "instrument_id": cls.instrument.id, "interval": "5m",
        })
        cls.other_instrument = cls.env["golok.lab.instrument"].create({
            "name": "Other Equity", "symbol": "OTHER", "exchange": "NSE", "company_id": cls.other_company.id,
        })
        cls.other_dataset = cls.env["golok.lab.dataset"].create({
            "name": "Other CSV", "source": "Test fixture", "origin": "synthetic",
            "instrument_id": cls.other_instrument.id, "interval": "5m", "company_id": cls.other_company.id,
        })
        cls.start = datetime(2024, 1, 2, 3, 50)

    def test_p08_fixture_session_scheduler_records_idempotent_phases(self):
        from datetime import timezone
        files = Path(__file__).parent / "fixtures/p02"
        schedule = json.loads((files / "spec.json").read_text())["schedule"]
        calendar = self.env["golok.lab.calendar"].with_user(self.admin).create({
            "name": "Phased fixture", "source": "Synthetic scheduler", "exchange": "NSE", "verification": "fixture",
            "verified_on": "2024-01-01", "schedule": json.dumps([*schedule, {"date": "2024-01-03", "kind": "closed"}])})
        dataset = self.env["golok.lab.dataset"].with_user(self.analyst).create({
            "name": "Scheduler sample", "source": "Synthetic scheduler", "origin": "synthetic",
            "instrument_id": self.instrument.id, "interval": "5m", "calendar_id": calendar.id})
        self.env["golok.lab.import"].with_user(self.analyst).create({
            "dataset_id": dataset.id, "upload": BinaryBytes((files / "candles.csv").read_bytes())}).action_import()
        watch = self.env["golok.lab.session.watch"].with_user(self.admin).create({"dataset_id": dataset.id})
        session = calendar._sessions()[datetime(2024, 1, 2).date()]
        cases = [(session.opening - timedelta(minutes=10), "pre_market"),
                 (session.opening + timedelta(minutes=10), "intraday"),
                 (session.closing + timedelta(minutes=1), "post_market"),
                 (datetime(2024, 1, 3, 12, tzinfo=timezone.utc), "closed")]
        for now, expected in cases:
            event = watch._dispatch(now)
            self.assertEqual(event.phase, expected)
            self.assertEqual(event, watch._dispatch(now))
            if expected in ("intraday", "post_market"):
                self.assertGreater(event.observation_count, 0)
                self.assertEqual(event.run_id.decision, "no_trade")
        replay_watch = watch.sudo()
        events = self.env["golok.lab.session.event"].sudo()
        events.search([("watch_id", "=", watch.id), ("phase", "=", "post_market")]).unlink()
        replay_watch.write({"checked_at": session.opening.replace(tzinfo=None)})
        watch._dispatch(cases[-1][0])
        recovered = events.search([("watch_id", "=", watch.id), ("recovered", "=", True)])
        self.assertEqual((recovered.phase, recovered.mode, recovered.run_id.as_of),
                         ("post_market", "fixture", session.closing.replace(tzinfo=None)))
        watch._dispatch(cases[-1][0])
        self.assertEqual(events.search_count([("watch_id", "=", watch.id), ("recovered", "=", True)]), 1)
        from unittest.mock import patch
        from odoo import fields
        now = cases[-1][0].replace(tzinfo=None)
        with patch.object(fields.Datetime, "now", return_value=now):
            action = watch.action_check_now()
            self.assertEqual(action["res_model"], "golok.lab.session.event")
            self.assertEqual(events.browse(action["res_id"]).phase, "closed")
            with self.assertRaises(AccessError):
                watch.with_user(self.analyst).action_check_now()
            watch.active = False
            self.assertFalse(watch.action_check_now())
            watch.active = True
            self.assertEqual(watch.action_check_now()["res_id"], action["res_id"])

        split = {**schedule[0], "date": "2024-01-04", "kind": "special", "open": "09:15", "close": "11:10",
                 "entry_cutoff": "10:40", "exit_cutoff": "11:05", "segments": [["09:15", "09:55"], ["10:30", "11:10"]]}
        split_calendar = self.env["golok.lab.calendar"].with_user(self.admin).create({
            "name": "Exceptional fixture", "source": "Synthetic scheduler", "exchange": "NSE", "verification": "fixture",
            "verified_on": "2024-01-01", "schedule": json.dumps([split])})
        split_dataset = self.env["golok.lab.dataset"].with_user(self.analyst).create({
            "name": "Exceptional sample", "source": "Synthetic exceptional", "origin": "synthetic",
            "instrument_id": self.instrument.id, "interval": "5m", "calendar_id": split_calendar.id})
        split_watch = self.env["golok.lab.session.watch"].with_user(self.admin).create({"dataset_id": split_dataset.id})
        split_session = split_calendar._sessions()[datetime(2024, 1, 4).date()]
        maintenance = split_watch._dispatch(split_session.windows()[0][1] + timedelta(minutes=1))
        self.assertEqual(maintenance.phase, "maintenance")
        self.assertFalse(maintenance.run_id)

    def test_p09_recurring_cycles_follow_new_completed_observations(self):
        from datetime import timezone

        files = Path(__file__).parent / "fixtures/p02"
        spec = json.loads((files / "spec.json").read_text())
        calendar = self.env["golok.lab.calendar"].with_user(self.admin).create({
            "name": "Recurring fixture", "source": "Test fixture", "exchange": "NSE", "verification": "fixture",
            "verified_on": "2024-01-01", "schedule": json.dumps(spec["schedule"]),
        })
        dataset = self.env["golok.lab.dataset"].with_user(self.analyst).create({
            "name": "Recurring cycle test", "source": "Incremental fixture", "origin": "synthetic",
            "instrument_id": self.instrument.id, "interval": "5m", "calendar_id": calendar.id,
        })
        header, first, second, third, *_tail = (files / "candles.csv").read_bytes().splitlines()
        importer = self.env["golok.lab.import"].with_user(self.analyst)
        watch = self.env["golok.lab.session.watch"].with_user(self.admin).create({
            "dataset_id": dataset.id, "cycle_minutes": 2,
        })
        session = calendar._sessions()[datetime(2024, 1, 2, tzinfo=timezone.utc).date()]
        cycles = self.env["golok.lab.research.cycle"]
        domain = [("watch_id", "=", watch.id)]
        importer.create({"dataset_id": dataset.id, "upload": BinaryBytes(b"\n".join((header, first)))}).action_import()
        summary = watch._dispatch(session.opening + timedelta(minutes=5))
        cycle = cycles.search(domain)
        self.assertEqual(cycle.state, "queued")
        self.assertEqual(watch._dispatch(session.opening + timedelta(minutes=7)), summary)
        self.assertEqual(cycles.search_count(domain), 1)
        jobs = self.env["golok.lab.research.job"].sudo()
        jobs._cron_run_next()
        self.assertEqual(cycle.state, "completed")
        self.assertEqual(cycle.candidate_ids.input_digest, cycle.run_id.input_digest)
        self.assertEqual(cycle.candidate_ids.evidence["decision"]["state"], "NO_TRADE")
        self.assertEqual(cycle.candidate_ids.lifecycle, "experimental")
        watch._dispatch(session.opening + timedelta(minutes=8))
        self.assertEqual(cycles.search_count(domain), 1)
        importer.create({"dataset_id": dataset.id, "upload": BinaryBytes(b"\n".join((header, second)))}).action_import()
        self.assertEqual(watch._dispatch(session.opening + timedelta(minutes=10)), summary)
        next_cycle = cycles.search(domain, limit=1)
        self.assertNotEqual(cycle, next_cycle)
        jobs._cron_run_next()
        self.assertNotEqual(cycle.candidate_ids.input_digest, next_cycle.candidate_ids.input_digest)
        with self.assertRaises(AccessError):
            next_cycle.candidate_ids.with_user(self.analyst).write({"reason": "forged"})
        importer.create({"dataset_id": dataset.id, "upload": BinaryBytes(b"\n".join((header, third)))}).action_import()
        watch._dispatch(session.opening + timedelta(minutes=15))
        watch.active = False
        jobs._cron_run_next()
        self.assertEqual(cycles.search(domain, limit=1).state, "blocked")
        self.assertEqual(cycles.search_count(domain), 3)
        self.assertEqual(watch.event_ids.filtered(lambda event: event.phase == "intraday"), summary)

    def test_p09_candidate_drives_observation_based_fixture_position(self):
        from datetime import timezone
        from unittest.mock import patch

        from odoo import fields

        files = Path(__file__).parent / "fixtures/p02"
        spec = json.loads((files / "spec.json").read_text())
        admin = self.env(user=self.admin.id)
        calendar = admin["golok.lab.calendar"].create({
            "name": "Automated paper calendar", "source": "Authored fixture", "exchange": "NSE",
            "verification": "fixture", "verified_on": "2024-01-01",
            "schedule": json.dumps([*spec["schedule"], {**spec["schedule"][0], "date": "2024-01-03"}]),
        })
        tariff = admin["golok.lab.tariff"].create({"name": "Automated paper tariff", "lines": json.dumps(spec["tariffs"])})
        dataset = admin["golok.lab.dataset"].create({
            "name": "Causal paper fixture", "source": "Authored fixture", "origin": "synthetic", "interval": "5m",
            "calendar_id": calendar.id, "instrument_id": self.instrument.id,
        })
        watch = admin["golok.lab.session.watch"].create({"dataset_id": dataset.id})
        second_instrument = admin["golok.lab.instrument"].create({
            "name": "Alternative paper asset", "symbol": "PAPERALT", "exchange": "NSE",
        })
        second_data = admin["golok.lab.dataset"].create({
            "name": "Competing paper fixture", "source": "Authored fixture", "origin": "synthetic", "interval": "5m",
            "calendar_id": calendar.id, "instrument_id": second_instrument.id,
        })
        second_watch = admin["golok.lab.session.watch"].create({"dataset_id": second_data.id})
        account = admin["golok.lab.fixture.account"].create({
            "name": "Automated fixture", "watch_ids": [(6, 0, (watch | second_watch).ids)],
            "tariff_id": tariff.id, "target_policy": "fixed_4r",
        })
        self.assertFalse(account.order_ids)
        header, *rows = (files / "candles.csv").read_bytes().splitlines()
        rows[5] = rows[5].replace(b",102,120,98,101,1000,", b",102,120,100,101,4000,")
        rows[6] = rows[6].replace(b",100,101,99,100,1000,", b",102,120,100,110,4000,")
        session = calendar._sessions()[datetime(2024, 1, 2, tzinfo=timezone.utc).date()]
        jobs = self.env["golok.lab.research.job"].sudo()

        def check(minutes, observations=(), *, work=False, selected_watch=watch, source_session=session):
            at = source_session.opening + timedelta(minutes=minutes)
            with patch.object(fields.Datetime, "now", return_value=at.replace(tzinfo=None)):
                if observations:
                    admin["golok.lab.import"].create({
                        "dataset_id": selected_watch.dataset_id.id, "upload": BinaryBytes(b"\n".join((header, *observations))),
                    }).action_import()
                selected_watch._dispatch(at)
                if work:
                    jobs._cron_run_next()

        check(20, rows[:4], work=True)
        account.invalidate_recordset()
        order = account.order_ids
        self.assertEqual(order.state, "pending", watch.cycle_ids.mapped("candidate_ids.reason"))
        self.assertEqual(order.candidate_id.lifecycle, "pending")
        self.assertEqual(order.candidate_id.evidence["decision"]["state"], "SIMULATION_CANDIDATE")
        self.assertGreater(account.reserved, 0)
        self.assertEqual(len(order.candidate_id.evidence["fixture_plan"]["signal_sha256"]), 64)
        check(20, rows[:4], work=True, selected_watch=second_watch)
        self.assertEqual(second_watch.cycle_ids.candidate_ids.reason, "EXPOSURE_EXISTS")
        self.assertEqual(second_watch.cycle_ids.candidate_ids.lifecycle, "rejected")
        self.assertEqual(len(account.order_ids), 1)
        with self.assertRaises(AccessError):
            watch.write({"paper_account_id": False})
        check(25, rows[4:5], work=True)
        self.assertEqual(order.state, "pending")
        check(30, rows[5:6], work=True)
        self.assertEqual(order.state, "open")
        self.assertEqual(order.entry_paise, 10200)
        self.assertGreater(order.entry_candle_id.open_time, order.candidate_id.generated_at)
        check(35, rows[6:7], work=True)
        self.assertEqual((order.state, order.exit_reason, order.candidate_id.lifecycle), ("closed", "TARGET", "closed"))
        self.assertGreater(order.net, 0)
        check(35, work=True)
        self.assertEqual((len(account.order_ids), account.entries), (1, 1))
        self.assertEqual(account.journal_ids.mapped("kind"), ["reserved", "opened", "closed"])
        self.assertEqual(account.available, account.opening + account.realized)
        check(50, rows[7:])
        self.assertEqual(watch.gap_ids[:1].missed, 1)
        self.assertEqual(watch.gap_ids[:1].resumed_at, (session.opening + timedelta(minutes=50)).replace(tzinfo=None))
        with self.assertRaises(ValidationError):
            account.action_reserve_fixture()
        following = calendar._sessions()[datetime(2024, 1, 3, tzinfo=timezone.utc).date()]
        following_rows = [row.replace(b"2024-01-02", b"2024-01-03") for row in rows]
        check(20, following_rows[:4], work=True, source_session=following)
        check(30, following_rows[4:6], work=True, source_session=following)
        outstanding = account.order_ids[:1]
        self.assertEqual(outstanding.state, "open")
        check(50, source_session=following)
        self.assertEqual(outstanding.state, "unresolved")
        self.assertEqual(outstanding.exit_reason, "MISSING_SQUARE_OFF_OBSERVATION")
        self.assertFalse(outstanding.exit_candle_id)
        self.assertGreater(account.position_cost, 0)

        expiry_data = admin["golok.lab.dataset"].create({
            "name": "Paper expiry fixture", "source": "Independent expiry fixture", "origin": "synthetic", "interval": "5m",
            "calendar_id": calendar.id, "instrument_id": self.instrument.id,
        })
        expiry_watch = admin["golok.lab.session.watch"].create({"dataset_id": expiry_data.id})
        expiry_account = admin["golok.lab.fixture.account"].create({
            "name": "Expiry fixture account", "watch_ids": [(6, 0, expiry_watch.ids)], "tariff_id": tariff.id,
            "target_policy": "fixed_4r",
        })
        check(20, following_rows[:4], work=True, source_session=following, selected_watch=expiry_watch)
        expired = expiry_account.order_ids
        self.assertEqual(expired.state, "pending")
        check(31, source_session=following, selected_watch=expiry_watch)
        self.assertEqual((expired.state, expired.candidate_id.lifecycle), ("cancelled", "expired"))
        self.assertEqual((expiry_account.available, expiry_account.reserved), (expiry_account.opening, 0))

    def test_p09_fixture_account_reservation_risk_and_journal(self):
        spec = json.loads((Path(__file__).parent / "fixtures/p02/spec.json").read_text())
        tariff = self.env["golok.lab.tariff"].with_user(self.admin).create({
            "name": "Prospective fixture tariff", "lines": json.dumps(spec["tariffs"]),
        })
        accounts = self.env["golok.lab.fixture.account"].with_user(self.admin)
        account = accounts.create({"name": "Target fixture", "tariff_id": tariff.id})
        with self.assertRaises(AccessError):
            account.with_user(self.analyst).action_reserve_fixture()
        self.assertEqual((account.opening, account.mode), (5000000, "fixture"))
        account.action_reserve_fixture()
        reserved = account.reserved
        self.assertGreater(reserved, 0)
        self.assertLessEqual(account.planned_risk, 25000)
        account.action_pause()
        self.assertEqual((account.available, account.reserved, account.order_ids.state), (5000000, 0, "cancelled"))
        with self.assertRaises(ValidationError):
            account.action_reserve_fixture()
        account.action_resume()
        account.action_reserve_fixture()
        account.action_open_fixture()
        account.action_open_fixture()
        self.assertEqual((account.reserved, account.position_cost, account.entries), (0, reserved, 1))
        account.action_close_fixture()
        account.action_close_fixture()
        self.assertGreater(account.realized, 0)
        self.assertEqual(account.available, account.opening + sum(account.journal_ids.mapped("delta_cash")))
        self.assertEqual(account.realized, sum(account.journal_ids.mapped("delta_net")))
        self.assertEqual(account.planned_risk, 0)
        with self.assertRaises(AccessError):
            account.journal_ids.with_user(self.analyst).write({"delta_cash": 42})
        losses = accounts.create({"name": "Loss fixture", "tariff_id": tariff.id, "scenario": "ambiguous"})
        for _ in range(2):
            losses.action_reserve_fixture()
            losses.action_open_fixture()
            losses.action_close_fixture()
        self.assertEqual((losses.state, losses.loss_streak), ("risk", 2))
        self.assertTrue(all(order.exit_paise == 9700 for order in losses.order_ids))
        missing = accounts.create({"name": "Unresolved fixture", "tariff_id": tariff.id, "scenario": "missing"})
        missing.action_reserve_fixture()
        missing.action_open_fixture()
        missing.action_close_fixture()
        self.assertEqual(missing.order_ids.state, "unresolved")
        self.assertGreater(missing.position_cost, 0)
        self.assertEqual(missing.realized, 0)
        for _ in range(2):
            account.action_reserve_fixture()
            account.action_open_fixture()
            account.action_close_fixture()
        self.assertEqual(account.entries, 3)
        with self.assertRaises(ValidationError):
            account.action_reserve_fixture()
        gap = accounts.create({"name": "Daily loss fixture", "tariff_id": tariff.id, "scenario": "severe_gap"})
        gap.action_reserve_fixture()
        gap.action_open_fixture()
        gap.action_close_fixture()
        self.assertEqual((gap.state, gap.loss_streak, gap.remaining_daily_risk), ("risk", 1, 0))
        self.assertLessEqual(gap.daily_realized, -50000)

    def test_p09_walk_forward_persists_reproducible_separated_folds(self):
        files = Path(__file__).parent / "fixtures/p02"
        spec = json.loads((files / "spec.json").read_text())
        schedule = [{**spec["schedule"][0], "date": f"2024-01-{number:02d}"} for number in range(2, 12)]
        setup = self.env(user=self.admin.id)
        calendar = setup["golok.lab.calendar"].create({
            "name": "Walk-forward fixture", "source": "Authored fixture", "exchange": "NSE", "verification": "fixture",
            "verified_on": "2024-01-01", "schedule": json.dumps(schedule),
        })
        tariff = setup["golok.lab.tariff"].create({"name": "Walk-forward costs", "lines": json.dumps(spec["tariffs"])})
        analyst = self.env(user=self.analyst.id)
        data = analyst["golok.lab.dataset"].create({
            "name": "Walk-forward sample", "source": "Authored sample", "origin": "synthetic", "interval": "5m",
            "instrument_id": self.instrument.id, "calendar_id": calendar.id,
        })
        header, rows = (files / "candles.csv").read_bytes().split(b"\n", 1)
        rows = rows.strip().replace(b",102,120,98,101,", b",102,120,100,101,")
        payload = header + b"\n" + b"\n".join(rows.replace(b"2024-01-02", item["date"].encode()) for item in schedule)
        analyst["golok.lab.import"].create({"dataset_id": data.id, "upload": BinaryBytes(payload)}).action_import()
        wizard = analyst["golok.lab.portfolio.wizard"].create({
            "dataset_ids": [(6, 0, data.ids)], "tariff_id": tariff.id, "starts": "2024-01-02",
            "ends": "2024-01-11", "validation_sessions": 2, "target_policy": "fixed_4r",
        })
        result = wizard.action_experiment()
        self.assertEqual(result["res_id"], wizard.action_experiment()["res_id"])
        record = analyst[result["res_model"]].browse(result["res_id"])
        self.assertEqual(record.fold_count, 4)
        rows = json.loads(record.report)["folds"]
        for fold in rows:
            self.assertEqual(len(fold["training_trials"]), 5)
            windows = fold["windows"]
            self.assertLess(windows["training"][-1], windows["validation"][0])
            self.assertLess(windows["validation"][-1], windows["evaluation"][0])
            self.assertEqual(fold["evaluation"]["strategy"], fold["selected"])
            self.assertEqual(fold["status"], "EVALUATED")
        with self.assertRaises(AccessError):
            record.action_review_promotion()
        approval = record.with_user(self.admin).action_review_promotion()
        review = setup[approval["res_model"]].browse(approval["res_id"])
        self.assertEqual(review.evidence["financial_validation"], "BLOCKED")
        self.assertEqual(review.frozen_sha256, record.fingerprint)
        wizard.target_policy = "causal_levels"
        grid_action = wizard.action_experiment()
        grid = analyst[grid_action["res_model"]].browse(grid_action["res_id"])
        self.assertEqual(grid.version, "r01-policy-grid-1")
        self.assertEqual(grid.id, wizard.action_experiment()["res_id"])
        for current in json.loads(grid.report)["folds"]:
            self.assertEqual(len(current["training_trials"]), 20)
            choices = {(trial["strategy"], trial["target_policy"]) for trial in current["training_trials"]}
            self.assertEqual(len(choices), 20)
            self.assertEqual(current["status"], "EVALUATED")
            for stage in ("validation", "evaluation"):
                result = current[stage]
                self.assertEqual(result["strategy"], current["selected"])
                self.assertEqual(result["target_policy"], current["selected_target_policy"])
                saved = analyst["golok.lab.portfolio"].browse(result["portfolio"])
                self.assertEqual(saved.starts.isoformat(), current["windows"][stage][0])

    def test_p08_source_conflict_blocks_research_and_is_idempotent(self):
        files = Path(__file__).parent / "fixtures/p02"
        schedule = json.loads((files / "spec.json").read_text())["schedule"]
        calendar = self.env["golok.lab.calendar"].with_user(self.admin).create({
            "name": "Comparison fixture", "source": "Authored fixture", "exchange": "NSE", "verification": "fixture",
            "verified_on": "2024-01-01", "schedule": json.dumps(schedule)})
        mapping = self.env["golok.lab.mapping"].with_user(self.admin).create({
            "instrument_id": self.instrument.id, "symbol": self.instrument.symbol, "provider": "manual",
            "token": "500", "starts": "2024-01-01", "tick": "0.05", "lot": 1, "listing_status": "listed",
            "source": "Authored fixture", "revision": "p08", "verification": "fixture", "isin": "IN0000000001"})
        sources = self.env["golok.lab.dataset"].with_user(self.analyst).create([
            {"name": label, "source": label, "origin": "synthetic", "interval": "5m",
             "instrument_id": self.instrument.id, "calendar_id": calendar.id, "mapping_id": mapping.id}
            for label in ("Source 1", "Source 2")])
        raw = (files / "candles.csv").read_bytes()
        header, first, rest = raw.split(b"\n", 2)
        columns = first.split(b",")
        columns[5] = str(int(columns[5]) + 1).encode()
        for dataset, payload in zip(sources, (raw, header + b"\n" + b",".join(columns) + b"\n" + rest)):
            self.env["golok.lab.import"].with_user(self.analyst).create({
                "dataset_id": dataset.id, "upload": BinaryBytes(payload)}).action_import()
        comparisons = self.env["golok.lab.source.comparison"].with_user(self.admin)
        params = {"left_id": sources[0].id, "right_id": sources[1].id, "close_at": self.start}
        match = comparisons.create({**params, "close_at": self.start + timedelta(minutes=5)})
        self.assertEqual(match.outcome, "UNKNOWN_LINEAGE")
        audit = comparisons.create(params)
        self.assertEqual(audit.outcome, "CONFLICT")
        self.assertEqual(json.loads(audit.differences)["volume"], 1)
        self.assertEqual(comparisons.create({**params, "left_id": sources[1].id, "right_id": sources[0].id}), audit)
        self.assertTrue(all(sources.mapped("integrity_conflict")))
        with self.assertRaises(AccessError):
            self.env["golok.lab.run"].with_user(self.analyst).create({"dataset_id": sources[0].id, "as_of": self.start})

    def _wizard(self, lines, dataset=None):
        raw = ("close_time,open,high,low,close,volume\n" + "\n".join(lines)).encode()
        return self.env["golok.lab.import"].with_user(self.analyst).create({
            "dataset_id": (dataset if dataset is not None else self.dataset).id,
            "upload": BinaryBytes(raw),
        })

    def _lines(self, count):
        return [
            f"{(self.start + timedelta(minutes=5 * index)).isoformat()}Z,100,103,99,101,{100 + index}"
            for index in range(count)
        ]

    def test_import_retry_and_atomic_conflict(self):
        lines = self._lines(3)
        self._wizard(lines[:2]).action_import()
        self._wizard(lines[:2]).action_import()
        model = self.env["golok.lab.candle"]
        self.assertEqual(model.search_count([("dataset_id", "=", self.dataset.id)]), 2)
        conflict = lines[1].replace(",101,", ",102,")
        with self.assertRaisesRegex(ValidationError, "stored candle differs"):
            self._wizard([conflict, lines[2]]).action_import()
        self.assertEqual(model.search_count([("dataset_id", "=", self.dataset.id)]), 2)
        self._wizard(lines).action_import()
        self.assertEqual(model.search_count([("dataset_id", "=", self.dataset.id)]), 3)

    def test_research_cutoff_evidence_and_no_trade(self):
        self._wizard(self._lines(25)).action_import()
        wizard = self.env["golok.lab.research"].with_user(self.analyst).create({
            "dataset_id": self.dataset.id, "as_of": self.start + timedelta(minutes=100),
        })
        action = wizard.action_research()
        runs = self.env["golok.lab.run"].with_user(self.viewer)
        run = runs.browse(action["res_id"])
        self.assertEqual(run.bar_count, 21)
        self.assertEqual(run.last_close, wizard.as_of)
        self.assertEqual(run.origin, "synthetic")
        self.assertEqual(run.decision, "no_trade")
        self.assertEqual(run.evidence["RE-01"]["finding"], "101")
        self.assertEqual(wizard.action_research()["res_id"], run.id)
        self.assertEqual(runs.overview()["last"]["id"], run.id)

    def test_gap_disables_findings(self):
        lines = self._lines(26)
        self._wizard(lines[:5] + lines[6:]).action_import()
        run = self.env["golok.lab.run"].with_user(self.analyst).create({
            "dataset_id": self.dataset.id, "as_of": self.start + timedelta(hours=5),
        })
        self.assertEqual(run.gap_count, 1)
        self.assertEqual(run.evidence["RE-01"]["status"], "INSUFFICIENT_DATA")
        self.assertEqual(run.decision, "no_trade")

    def test_permissions_and_company_scope(self):
        candles = self.env["golok.lab.candle"]
        runs = self.env["golok.lab.run"]
        self._wizard(self._lines(1)).action_import()
        other_wizard = self.env["golok.lab.import"].create({
            "dataset_id": self.other_dataset.id,
            "upload": self._wizard(self._lines(1)).upload,
        })
        other_wizard.action_import()
        own_run = runs.with_user(self.analyst).create({
            "dataset_id": self.dataset.id, "as_of": self.start,
        })
        runs.create({"dataset_id": self.other_dataset.id, "as_of": self.start})
        self.assertEqual(candles.with_user(self.viewer).search_count([]), 1)
        self.assertEqual(runs.with_user(self.viewer).search([]), own_run.with_user(self.viewer))
        self.assertEqual(runs.with_user(self.viewer).overview()["datasets"], 1)
        with self.assertRaises(AccessError):
            self.other_dataset.with_user(self.viewer).check_access("read")
        with self.assertRaises(AccessError):
            self.dataset.with_user(self.viewer).write({"name": "Unauthorized"})
        with self.assertRaises(AccessError):
            candles.with_user(self.analyst).create({"dataset_id": self.dataset.id})
        with self.assertRaises(AccessError):
            own_run.write({"reason": "Retrospective edit"})
        with self.assertRaises(AccessError):
            runs.with_user(self.analyst).create({"dataset_id": self.other_dataset.id, "as_of": self.start})
        with self.assertRaises((AccessError, ValidationError)):
            self._wizard(self._lines(1), self.other_dataset).action_import()

    def test_database_duplicate_constraint(self):
        self._wizard(self._lines(1)).action_import()
        model = self.env["golok.lab.candle"]
        record = model.search([("dataset_id", "=", self.dataset.id)])
        from psycopg2.errors import UniqueViolation

        with self.assertRaises(UniqueViolation), self.env.cr.savepoint():
            model.create(record.copy_data()[0])

    def test_point_in_time_calendar_quarantine_and_chart(self):
        revisions = self.env["golok.lab.calendar"]
        vals = {
            "name": "Calendar test 01", "source": "Synthetic fixture", "exchange": "NSE",
            "verification": "fixture", "verified_on": "2024-01-01",
            "schedule": json.dumps([{"date": "2024-01-02", "kind": "regular", "open": "09:15",
                                     "close": "15:30", "entry_cutoff": "14:30", "exit_cutoff": "15:25"}]),
        }
        with self.assertRaises(AccessError):
            revisions.with_user(self.analyst).create(vals)
        revision = revisions.with_user(self.admin).create(vals)
        with self.assertRaises(AccessError):
            revision.write({"name": "Retrospective edit"})
        dataset = self.env["golok.lab.dataset"].with_user(self.analyst).create({
            "name": "Timed fixture", "source": "Timed fixture", "origin": "synthetic",
            "instrument_id": self.instrument.id, "interval": "5m", "calendar_id": revision.id,
        })
        header = "close_time,open,high,low,close,volume,open_time,available_at\n"
        rows = ("2024-01-02T09:20:00+05:30,100,103,99,101,100,2024-01-02T09:15:00+05:30,2024-01-02T09:22:00+05:30\n"
                "2024-01-02T09:25:00+05:30,101,103,99,102,110,2024-01-02T09:20:00+05:30,2024-01-02T09:28:00+05:30\n")
        imports = self.env["golok.lab.import"].with_user(self.analyst)
        bad = imports.create({"dataset_id": dataset.id, "upload": BinaryBytes((header + rows.replace("09:15", "09:14")).encode())})
        with self.assertRaisesRegex(ValidationError, "outside the session"):
            bad.action_import()
        wizard = imports.create({"dataset_id": dataset.id, "upload": BinaryBytes((header + rows).encode())})
        wizard.action_import()
        self.assertIn("0 inserted", wizard.action_import()["params"]["message"])
        model = self.env["golok.lab.run"].with_user(self.analyst)
        run = model.create({"dataset_id": dataset.id, "as_of": "2024-01-02 03:56:00"})
        self.assertEqual(run.bar_count, 1)
        self.assertEqual(run.engine_version, "2")
        self.assertEqual(run.decision, "no_trade")
        viewer = model.with_user(self.viewer)
        self.assertEqual(viewer.chart_data(run.id)["bars"][0][4], "101")
        with self.assertRaises(AccessError):
            viewer.create({"dataset_id": dataset.id, "as_of": "2024-01-02 03:56:00"})
        with self.assertRaises(ValidationError):
            dataset.action_toggle_quarantine()
        dataset.with_user(self.admin).action_toggle_quarantine()
        self.assertIsNone(viewer.chart_data(run.id))
        with self.assertRaises(ValidationError):
            wizard.action_import()

    def test_p03_mapping_date_scope_and_database_exclusions(self):
        from psycopg2.errors import ExclusionViolation
        mappings = self.env["golok.lab.mapping"].with_user(self.admin)
        vals = {"instrument_id": self.instrument.id, "symbol": "ORIGINAL", "provider": "manual",
                "token": "100", "starts": "2024-01-01", "ends": "2024-01-03", "tick": "0.05", "lot": 1,
                "listing_status": "listed", "source": "Synthetic reference", "revision": "v1", "verification": "fixture"}
        first = mappings.create(vals)
        self.assertEqual(first.exchange, "NSE")
        with self.assertRaises(ExclusionViolation), self.env.cr.savepoint():
            mappings.create({**vals, "starts": "2024-01-02", "ends": "2024-01-04", "symbol": "CHANGED"})
        mappings.create({**vals, "starts": "2024-01-03", "ends": False, "symbol": "RENAMED"})
        with self.assertRaises(AccessError):
            mappings.with_user(self.analyst).create(vals)
        with self.assertRaises(AccessError):
            first.write({"symbol": "REWRITE"})
        with self.assertRaises(ValidationError):
            mappings.create({**vals, "instrument_id": self.other_instrument.id})
        other = mappings.sudo().create({**vals, "instrument_id": self.other_instrument.id})
        self.assertNotIn(other.id, mappings.with_user(self.viewer).search([]).ids)

    def test_p03_synthetic_workflow_and_reproducible_immutable_results(self):
        files = Path(__file__).parent / "fixtures/p02"
        spec = json.loads((files / "spec.json").read_text())
        second = {**spec["schedule"][0], "date": "2024-01-03"}
        calendar = self.env["golok.lab.calendar"].with_user(self.admin).create({
            "name": "Synthetic experiment calendar", "source": "Synthetic fixture", "exchange": "NSE",
            "verification": "fixture", "verified_on": "2024-01-01",
            "schedule": json.dumps([*spec["schedule"], second]),
        })
        dataset = self.env["golok.lab.dataset"].with_user(self.analyst).create({
            "name": "Two synthetic sessions", "source": "Synthetic P03 fixture", "origin": "synthetic",
            "instrument_id": self.instrument.id, "interval": "5m", "calendar_id": calendar.id,
        })
        tariff = self.env["golok.lab.tariff"].with_user(self.admin).create({
            "name": "Synthetic fees", "lines": json.dumps(spec["tariffs"]),
        })
        payload = (files / "candles.csv").read_bytes()
        _, rows = payload.split(b"\n", 1)
        self.env["golok.lab.import"].with_user(self.analyst).create({
            "dataset_id": dataset.id,
            "upload": BinaryBytes(payload.rstrip() + b"\n" + rows.replace(b"2024-01-02", b"2024-01-03")),
        }).action_import()
        wizard = self.env["golok.lab.experiment.wizard"].with_user(self.analyst).create({
            "dataset_id": dataset.id, "tariff_id": tariff.id, "starts": "2024-01-02", "ends": "2024-01-03",
        })
        action = wizard.action_run()
        self.assertEqual(action["res_id"], wizard.action_run()["res_id"])
        experiment = self.env[action["res_model"]].with_user(self.analyst).browse(action["res_id"])
        result = json.loads(experiment.result)
        self.assertEqual(experiment.status, "completed")
        self.assertEqual(experiment.trade_count, 2)
        self.assertEqual(set(json.loads(experiment.specification)["code_digests"]),
                         {"experiments", "backtest", "calendar", "simulation"})
        self.assertEqual([day["status"] for day in result["days"]], ["REPLAYED", "REPLAYED"])
        self.assertEqual(result["metrics"]["consecutive_losses"], 2)
        with self.assertRaises(AccessError):
            experiment.write({"result": "{}"})
        with self.assertRaises(ValidationError):
            self.env[experiment._name].with_user(self.analyst).create({"status": "completed"})
        accounts = self.env["golok.lab.paper.account"].with_user(self.admin)
        account = accounts.create({"name": "Synthetic virtual test"})
        with self.assertRaises(AccessError):
            account.with_user(self.analyst)._post_replay(experiment)
        wizard = self.env["golok.lab.paper.wizard"].with_user(self.admin).create(
            {"account_id": account.id, "experiment_id": experiment.id}
        )
        posting = wizard.action_post()
        self.assertEqual(posting["res_id"], wizard.action_post()["res_id"])
        batch = self.env[posting["res_model"]].with_user(self.viewer).browse(posting["res_id"])
        self.assertEqual(len(batch.event_ids), 6)
        self.assertEqual(sum(batch.event_ids.mapped("reserved_delta")), 0)
        self.assertEqual(sum(batch.event_ids.mapped("quantity_delta")), 0)
        self.assertEqual(batch.before_paise + sum(batch.event_ids.mapped("cash_delta")), batch.after_paise)
        self.assertEqual(batch.after_paise, account.available_paise)
        with self.assertRaises(AccessError):
            account.write({"available_paise": 1})
        with self.assertRaises(ValidationError):
            accounts.create({"name": "Forged", "available_paise": 1})
        tiny = accounts.create({"name": "Insufficient fixture cash", "initial_deposit": "1.00"})
        with self.assertRaisesRegex(ValidationError, "Frozen starting capital"):
            tiny._post_replay(experiment)
        self.assertEqual(tiny.available_paise, 100)
        self.assertFalse(self.env["golok.lab.paper.batch"].search([("account_id", "=", tiny.id)]))

    def test_p03_supplemental_findings_and_offline_provider_setup(self):
        from unittest.mock import patch

        self._wizard(self._lines(21)).action_import()
        run = self.env["golok.lab.run"].with_user(self.analyst).create({
            "dataset_id": self.dataset.id, "as_of": "2024-01-02 06:00:00",
        })
        action = run.action_supplemental_findings()
        finding = self.env[action["res_model"]].with_user(self.viewer).browse(action["res_id"])
        self.assertEqual(finding.input_digest, run.input_digest)
        self.assertEqual(json.loads(finding.findings)["RE-06"]["finding"]["rolling_support"], "99")
        with self.assertRaises(AccessError):
            run.with_user(self.viewer).action_supplemental_findings()
        setup = self.env["golok.lab.provider.setup"].with_user(self.admin).create({})
        with patch.dict("os.environ", {"GOLOK_SMARTAPI_AUTHORIZED": "0"}):
            setup.action_check_configuration()
            setup.action_test_authentication()
        self.assertEqual(setup.status, "OFFLINE")
        with self.assertRaises(ValidationError):
            setup.write({"status": "CONNECTED"})
        with self.assertRaises(ValidationError):
            self.env[setup._name].with_user(self.admin).create({"status": "CONNECTED"})
        with self.assertRaises(AccessError):
            self.env[setup._name].with_user(self.analyst).create({})
        with patch.dict("os.environ", {"GOLOK_UPSTOX_AUTHORIZED": "1",
                                       "GOLOK_UPSTOX_ANALYTICS_TOKEN": "authored-test-value"}):
            setup.action_check_upstox()
        self.assertEqual(setup.status, "REVIEW REQUIRED")
        self.assertIn("Company historical import permission current: No", setup.details)
        self.assertNotIn("authored-test-value", setup.details)

    def test_p03_job_worker_and_immutable_corporate_source(self):
        actions = self.env["golok.lab.corporate.action"].with_user(self.admin)
        action = actions.create({"name": "Synthetic split", "instrument_id": self.instrument.id,
                                 "kind": "split", "effective": "2024-01-02", "published_at": "2024-01-01 12:00:00",
                                 "source": "Fixture notice", "revision": "v1", "numerator": 2, "denominator": 1})
        with self.assertRaises(AccessError):
            action.write({"numerator": 3})
        jobs = self.env["golok.lab.research.job"]
        researcher = jobs.with_user(self.analyst)
        vals = {"dataset_id": self.dataset.id, "cutoff": "2024-01-02 04:00:00"}
        job = researcher.create(vals)
        self.assertEqual(job, researcher.create(vals))
        rejected = researcher.create({**vals, "cutoff": "2024-01-02 04:05:00"})
        self.assertTrue(rejected.action_cancel())
        self.assertTrue(rejected.action_cancel())
        jobs._cron_run_next()
        self.assertEqual(job.state, "completed")
        self.assertEqual(job.run_id.decision, "no_trade")
        self.assertEqual(rejected.state, "cancelled")
        self.assertEqual(job.requested_by, self.analyst)
        failed = researcher.create({**vals, "cutoff": "2024-01-02 04:10:00"})
        failed.sudo().write({"state": "failed", "attempts": 1, "failure_reason": "Authored failure fixture"})
        self.assertTrue(failed.action_retry())
        self.assertTrue(failed.action_retry())
        self.assertEqual(failed.state, "queued")
        self.assertEqual(failed.attempts, 1)

    def test_p04_fixture_sync_atomic_viewable_and_idempotent(self):
        mapping = self.env["golok.lab.mapping"].with_user(self.admin).create({
            "instrument_id": self.instrument.id, "symbol": self.instrument.symbol, "provider": "smartapi",
            "token": "123", "starts": "2024-01-02", "ends": "2024-01-03", "tick": "0.05", "lot": 1,
            "listing_status": "listed", "source": "Synthetic source", "revision": "fixture", "verification": "fixture",
        })
        revision = self.env["golok.lab.calendar"].with_user(self.admin).create({
            "name": "Sync fixture", "source": "Synthetic fixture", "exchange": "NSE", "verification": "fixture",
            "verified_on": "2024-01-02", "schedule": json.dumps([{
                "date": "2024-01-02", "kind": "regular", "open": "09:15", "close": "09:25",
                "entry_cutoff": "09:20", "exit_cutoff": "09:25"}]),
        })
        model = self.env["golok.lab.sync.wizard"].with_user(self.admin)
        reports = self.env["golok.lab.sync"].with_user(self.viewer)
        vals = {"mapping_id": mapping.id, "calendar_id": revision.id, "day": "2024-01-02", "interval": "5m"}
        rows = [["2024-01-02T09:15:00+05:30", 100, 103, 99, 100, 10],
                ["2024-01-02T09:20:00+05:30", 100, 103, 99, 101, 20]]

        def submit(response, **extra):
            action = model.create({**vals, **extra, "fixture_rows": json.dumps(response)}).action_sync()
            return reports.browse(action["res_id"])

        for malformed in ([], rows[:1], [rows[0], rows[0]], [rows[0], ["bad"]]):
            self.assertEqual(submit(malformed).state, "rejected")
        first = submit(rows)
        self.assertEqual((first.state, first.count, first.inserted, first.dataset_id.origin), ("complete", 2, 2, "synthetic"))
        self.assertEqual(submit(rows).inserted, 0)
        self.assertEqual(submit([rows[0], [*rows[1][:-1], 21]]).state, "rejected")
        self.assertEqual(submit(rows, day="2024-01-03").state, "rejected")
        self.assertEqual(self.env["golok.lab.candle"].search_count([("dataset_id", "=", first.dataset_id.id)]), 2)
        with self.assertRaises(AccessError):
            model.with_user(self.analyst).create(vals)
        with self.assertRaises(AccessError):
            self.env["golok.lab.dataset"].with_user(self.analyst).create({"origin": "provider"})

        plans = self.env["golok.lab.sync.plan"].with_user(self.admin)
        other = self.env["golok.lab.instrument"].with_user(self.admin).create({
            "name": "Plan Equity", "symbol": "PLAN", "exchange": "NSE",
        })
        third = self.env["golok.lab.instrument"].with_user(self.admin).create({
            "name": "Other Plan Equity", "symbol": "PLAN2", "exchange": "NSE",
        })
        second = mapping.copy({"instrument_id": other.id, "symbol": other.symbol, "token": "456", "ends": "2024-01-04"})
        third_mapping = mapping.copy({
            "instrument_id": third.id, "symbol": third.symbol, "token": "789", "ends": "2024-01-04",
        })
        first_day = json.loads(revision.schedule)[0]
        both = revision.copy({"name": "Two closed historical sessions",
                              "schedule": json.dumps([first_day, {**first_day, "date": "2024-01-03"}])})
        next_rows = [[row[0].replace("2024-01-02", "2024-01-03"), *row[1:]] for row in rows]
        plan_vals = {"name": "Two instruments and two sessions", "starts": "2024-01-02", "ends": "2024-01-03",
                     "mapping_ids": [(6, 0, [second.id, third_mapping.id])], "calendar_ids": [(6, 0, both.ids)],
                     "fixture_input": json.dumps({f"{item.id}/{day}": samples for item in (second, third_mapping)
                                                  for day, samples in (("2024-01-02", rows), ("2024-01-03", next_rows))})}
        with self.assertRaises(AccessError):
            plans.with_user(self.viewer).create(plan_vals)
        plan = plans.create(plan_vals)
        self.assertEqual(plan.task_ids.mapped("state"), ["queued"] * 4)
        plan.action_process_next()
        self.assertEqual(plan.task_ids.mapped("state"), ["done", "queued", "queued", "queued"])
        self.assertEqual(plan.task_ids[0].report_id.inserted, 2)
        for _ in range(3):
            plan.invalidate_recordset()
            plans.browse(plan.id).action_process_next()
        self.assertEqual(plan.state, "done")
        self.assertEqual(plan.task_ids[1].report_id.inserted, 2)
        self.assertFalse(any(plan.task_ids.mapped("fixture_rows")))
        with self.assertRaises(AccessError):
            plan.write({"state": "queued"})
        cancelled = plans.create(plan_vals)
        cancelled.action_process_next()
        self.assertEqual(cancelled.task_ids[0].report_id.inserted, 0)
        cancelled.action_cancel()
        cancelled.action_process_next()
        self.assertEqual(cancelled.task_ids.mapped("state"), ["done", "cancelled", "cancelled", "cancelled"])

    def test_p06p07_r01_upstox_fixture_and_automatic_comparison(self):
        mappings = self.env["golok.lab.mapping"].with_user(self.admin)
        base = {"instrument_id": self.instrument.id, "symbol": self.instrument.symbol,
                "starts": "2024-01-02", "tick": "0.05", "listing_status": "listed",
                "source": "Authored fixture", "revision": "r01", "verification": "fixture", "isin": "IN0000000001"}
        smart = mappings.create({**base, "provider": "smartapi", "token": "123"})
        upstox = mappings.create({**base, "provider": "upstox", "token": "NSE_EQ|IN0000000001"})
        revision = self.env["golok.lab.calendar"].with_user(self.admin).create({
            "name": "Comparison fixture", "source": "Authored fixture", "exchange": "NSE", "verification": "fixture",
            "verified_on": "2024-01-02", "schedule": json.dumps([{
                "date": "2024-01-02", "kind": "regular", "open": "09:15", "close": "09:25",
                "entry_cutoff": "09:20", "exit_cutoff": "09:25"}]),
        })
        wizard = self.env["golok.lab.sync.wizard"].with_user(self.admin)
        reports = self.env["golok.lab.sync"].with_user(self.admin)
        common = {"calendar_id": revision.id, "day": "2024-01-02", "interval": "5m"}
        rows = [["2024-01-02T09:15:00+05:30", 100, 103, 99, 100, 10],
                ["2024-01-02T09:20:00+05:30", 100, 103, 99, 101, 20]]

        def submit(mapping, payload):
            result = wizard.create({**common, "mapping_id": mapping.id, "fixture_rows": json.dumps(payload)}).action_sync()
            return reports.browse(result["res_id"])

        first = submit(smart, rows)
        self.assertEqual(first.state, "complete")
        data = {"status": "success", "data": {"candles": [[*rows[1][:-1], 21, 0], [*rows[0], 0]]}}
        plan_vals = {"name": "Upstox comparison", "starts": "2024-01-02", "ends": "2024-01-02",
                     "mapping_ids": [(6, 0, upstox.ids)], "calendar_ids": [(6, 0, revision.ids)],
                     "fixture_input": json.dumps({f"{upstox.id}/2024-01-02": data})}
        plans = self.env["golok.lab.sync.plan"].with_user(self.admin)
        with self.assertRaises(ValidationError), self.env.cr.savepoint():
            plans.create({**plan_vals, "interval": "30m"})
        plan = plans.create(plan_vals)
        plan.action_process_next()
        self.assertEqual(plan.state, "done")
        self.assertFalse(plan.task_ids.fixture_rows)
        second = plan.task_ids.report_id
        self.assertEqual((second.state, second.count, second.reason), ("complete", 2, "SOURCE_CONFLICT_QUARANTINED"))
        audits = self.env["golok.lab.source.comparison"].with_user(self.admin).search([
            ("left_id", "=", first.dataset_id.id), ("right_id", "=", second.dataset_id.id)])
        self.assertCountEqual(audits.mapped("outcome"), ["UNKNOWN_LINEAGE", "CONFLICT"])
        for dataset in (first.dataset_id, second.dataset_id):
            self.assertTrue(dataset.integrity_conflict)
            with self.assertRaises(AccessError):
                dataset._permit("research")
        self.assertEqual(submit(upstox, data).state, "rejected")

    def test_p05_portfolio_fixture_and_role_boundaries(self):
        files = Path(__file__).parent / "fixtures/p02"
        spec = json.loads((files / "spec.json").read_text())
        revision = self.env["golok.lab.calendar"].with_user(self.admin).create({
            "name": "Synthetic portfolio calendar", "source": "Fixture", "exchange": "NSE",
            "verification": "fixture", "verified_on": "2024-01-01", "schedule": json.dumps([
                {**spec["schedule"][0], "date": f"2024-01-0{day}"} for day in range(2, 6)]),
        })
        tariff = self.env["golok.lab.tariff"].with_user(self.admin).create({
            "name": "Synthetic portfolio tariff", "lines": json.dumps(spec["tariffs"]),
        })
        second = self.env["golok.lab.instrument"].with_user(self.admin).create({
            "name": "Second portfolio instrument", "symbol": "SECOND", "exchange": "NSE",
        })
        datasets = self.env["golok.lab.dataset"].with_user(self.analyst).create([{
            "name": instrument.name, "source": "P05 fixture", "origin": "synthetic",
            "instrument_id": instrument.id, "interval": "5m", "calendar_id": revision.id,
        } for instrument in self.instrument | second])
        header, observations = (files / "candles.csv").read_bytes().split(b"\n", 1)
        payload = header + b"\n" + b"\n".join(observations.strip().replace(b"2024-01-02", f"2024-01-0{n}".encode())
                                             for n in range(2, 6))
        for dataset in datasets:
            self.env["golok.lab.import"].with_user(self.analyst).create({
                "dataset_id": dataset.id, "upload": BinaryBytes(payload),
            }).action_import()
        vals = {"dataset_ids": datasets.ids, "tariff_id": tariff.id, "starts": "2024-01-02", "ends": "2024-01-02",
                "capital": "50000", "tick": "0.05", "strategy": "ST-01", "target_policy": "fixed_4r"}
        portfolios = self.env["golok.lab.portfolio"].with_user(self.analyst)
        record = portfolios.create(vals)
        self.assertEqual(record, portfolios.create({**vals, "dataset_ids": list(reversed(datasets.ids))}))
        self.assertEqual(self.env["golok.lab.run"].with_user(self.viewer).overview()["portfolios"], 1)
        result = json.loads(record.with_user(self.viewer).result)
        publication = record.action_calculate_performance()
        metrics = self.env[publication["res_model"]].with_user(self.analyst).browse(publication["res_id"])
        self.assertEqual(metrics.id, record.action_calculate_performance()["res_id"])
        summary = json.loads(metrics.report)
        self.assertEqual(summary["trade_count"], record.trade_count)
        self.assertEqual(Decimal(summary["net"]), Decimal(result["net"]))
        self.assertGreater(summary["mark_samples"], 0)
        self.assertIn("amount", summary["intraday_mark_to_market_drawdown"])
        fingerprints = {item["asset"]: item["input_digest"] for item in json.loads(record.specification)["inputs"]}
        self.assertTrue(all(row["gates"]["G01"]["dataset_version"] == fingerprints[row["asset"]]
                            for row in result["decisions"]))
        wizard = self.env["golok.lab.portfolio.wizard"].with_user(self.analyst).create({
            **vals, "dataset_ids": [(6, 0, datasets.ids)]})
        comparison = wizard.action_compare()
        self.assertEqual(len(portfolios.search(comparison["domain"])), 5)
        wizard.ends = "2024-01-05"
        validation = portfolios.search(wizard.action_walk_forward()["domain"])
        self.assertEqual(str(validation.starts), "2024-01-05")
        self.assertEqual(validation.starts, validation.ends)
        wizard.write({"starts": "2024-01-04", "ends": "2024-01-04", "training_id": record.id})
        seal_action = wizard.action_seal()
        seal = self.env["golok.lab.holdout"].with_user(self.admin).browse(seal_action["res_id"])
        self.assertFalse(seal.result_id)
        candles = self.env["golok.lab.candle"].with_user(self.viewer)
        restricted = [("dataset_id", "in", wizard.dataset_ids.ids), ("close_time", ">=", "2024-01-04 00:00:00"),
                      ("close_time", "<", "2024-01-05 00:00:00")]
        raw = candles.sudo().search(restricted, limit=1)
        self.assertTrue(raw)
        self.assertFalse(candles.search(restricted))
        with self.assertRaises(AccessError):
            candles.browse(raw.id).read(["close_price"])
        self.viewer.sudo().write({"group_ids": [(4, self.env.ref("base.group_allow_export").id)]})
        with self.assertRaises(AccessError):
            candles.browse(raw.id).export_data(["close_price"])
        with self.assertRaises(ValidationError):
            wizard.action_run()
        with self.assertRaises(AccessError):
            seal.with_user(self.analyst).action_consume()
        self.assertEqual(seal.action_consume()["res_id"], seal.result_id.id)
        with self.assertRaises(ValidationError):
            seal.action_consume()
        with self.assertRaises(ValidationError):
            wizard.action_seal()
        self.assertGreaterEqual(len(result["decisions"]), 2)
        self.assertGreaterEqual(len(result["trades"]), 1)
        self.assertEqual(Decimal(result["initial_cash"]) + sum(Decimal(row["delta"]) for row in result["ledger"]),
                         Decimal(result["ending_cash"]))
        self.assertEqual(Decimal(result["gross"]) - Decimal(result["fees"]), Decimal(result["net"]))
        with self.assertRaises(AccessError):
            record.write({"result": "{}"})
        with self.assertRaises(AccessError):
            portfolios.with_user(self.viewer).create(vals)
        with self.assertRaises(AccessError):
            portfolios.create({**vals, "dataset_ids": self.other_dataset.ids})

    def test_p05_provider_diagnostics_reuse_session_and_do_not_auto_login(self):
        from datetime import timezone
        from unittest.mock import Mock, patch

        from ..models import provider
        from ..services.smartapi import ProviderError

        setup = self.env["golok.lab.provider.setup"].with_user(self.admin).create({})
        sync = self.env["golok.lab.sync"].with_user(self.admin)
        client = Mock(state="AUTH_REQUIRED")
        config = dict.fromkeys(provider._IDENTITY_ENV, "fixture")
        config.update({"GOLOK_SMARTAPI_AUTHORIZED": "1", "GOLOK_SMARTAPI_HISTORY_OPEN_STAMPED": "1",
                       "GOLOK_SMARTAPI_TOTP_ISSUED_AT": "2000-01-01T00:00:00+00:00"})
        credentials = ("fixture", "fixture", "000000")
        with (
            patch.dict("os.environ", config),
            patch.object(provider, "_SESSIONS", {}),
            patch.object(type(setup), "_configuration", return_value=(client, credentials, "", "")),
            patch.object(type(self.env["golok.lab.provider.budget"]), "_reserve_auth", return_value=True),
        ):
            with self.assertRaisesRegex(ProviderError, "AUTH_REQUIRED"):
                sync._client()
            setup.action_test_authentication()
            self.assertEqual(setup.status, "AUTHORIZATION REQUIRED")
            client.authenticate.assert_not_called()
            with patch.dict("os.environ", {"GOLOK_SMARTAPI_TOTP_ISSUED_AT": datetime.now(timezone.utc).isoformat()}):
                setup.action_test_authentication()
            self.assertEqual(setup.status, "AUTHENTICATED")
            self.assertIs(sync._client(), client)
            setup.action_test_authentication()
            client.authenticate.assert_called_once_with(*credentials)
            with patch.dict("os.environ", {"GOLOK_SMARTAPI_AUTHORIZED": "0"}):
                with self.assertRaisesRegex(ProviderError, "LOCAL_AUTHORIZATION_REQUIRED"):
                    sync._client()
            with self.assertRaisesRegex(ProviderError, "AUTH_REQUIRED"):
                sync._client()
