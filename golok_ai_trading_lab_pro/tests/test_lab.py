import json
from datetime import datetime, timedelta
from pathlib import Path

from odoo.exceptions import AccessError, ValidationError
from odoo.tests import TransactionCase, new_test_user, tagged
from odoo.tools.binary import BinaryBytes

MODULE = "golok_ai_trading_lab_pro"


@tagged("at_install", "-post_install")
class TestLab(TransactionCase):
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
        with self.assertRaises(ValidationError):
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
        with self.assertRaises(AccessError):
            self.env[setup._name].with_user(self.analyst).create({})

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
        rejected.action_cancel()
        jobs._cron_run_next()
        self.assertEqual(job.state, "completed")
        self.assertEqual(job.run_id.decision, "no_trade")
        self.assertEqual(rejected.state, "cancelled")
        self.assertEqual(job.requested_by, self.analyst)
