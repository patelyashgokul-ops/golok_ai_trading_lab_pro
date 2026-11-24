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
    def test_p06_review_and_daily_fixture(self):
        import base64
        from ..services.bhavcopy import COLUMNS

        reviews = self.env["golok.lab.source.review"].with_user(self.admin)
        imports = self.env["golok.lab.daily.import"].with_user(self.admin)
        calendar = self.env["golok.lab.calendar"].with_user(self.admin).create({
            "name": "Daily fixture", "source": "Synthetic", "exchange": "NSE", "verification": "fixture",
            "verified_on": "2024-01-01", "schedule": json.dumps([{"date": "2024-01-02", "kind": "regular",
                "open": "09:15", "close": "15:30", "entry_cutoff": "14:30", "exit_cutoff": "15:20"}]),
        })
        payload = ",".join(COLUMNS) + "\nDEMO,EQ,10,12,9,11,11,10,100,1000,02-JAN-2024,4,IN0000000001"
        vals = {"source": "fixture", "day": "2024-01-02", "calendar_id": calendar.id,
                "upload": base64.b64encode(payload.encode()).decode()}
        with self.assertRaises(AccessError):
            imports.create(vals)
        grant = {"provider": "fixture", "terms_url": "fixture", "documentation": "fixture",
                 "evidence": "Self-authored OHLC", "purpose": "Software testing", "restrictions": "Synthetic only",
                 "expires": "2099-01-01", "display": True, "query": True, "persist": True}
        reviews.create(grant)
        accepted = imports.create(vals)
        self.assertEqual((accepted.status, accepted.count), ("accepted", 1))
        self.assertEqual(accepted, imports.create(vals))
        self.assertEqual(imports.create({**vals, "upload": "eA=="}).status, "quarantine")
        with self.assertRaises(AccessError):
            imports.with_user(self.viewer).create(vals)
        reviews.create({**grant, "persist": False})
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

    def test_p05_portfolio_fixture_and_role_boundaries(self):
        files = Path(__file__).parent / "fixtures/p02"
        spec = json.loads((files / "spec.json").read_text())
        revision = self.env["golok.lab.calendar"].with_user(self.admin).create({
            "name": "Synthetic portfolio calendar", "source": "Fixture", "exchange": "NSE",
            "verification": "fixture", "verified_on": "2024-01-01", "schedule": json.dumps(spec["schedule"]),
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
        for dataset in datasets:
            self.env["golok.lab.import"].with_user(self.analyst).create({
                "dataset_id": dataset.id, "upload": BinaryBytes((files / "candles.csv").read_bytes()),
            }).action_import()
        vals = {"dataset_ids": datasets.ids, "tariff_id": tariff.id, "starts": "2024-01-02", "ends": "2024-01-02",
                "capital": "50000", "tick": "0.05", "strategy": "ST-01"}
        portfolios = self.env["golok.lab.portfolio"].with_user(self.analyst)
        record = portfolios.create(vals)
        self.assertEqual(record, portfolios.create({**vals, "dataset_ids": list(reversed(datasets.ids))}))
        self.assertEqual(self.env["golok.lab.run"].with_user(self.viewer).overview()["portfolios"], 1)
        result = json.loads(record.with_user(self.viewer).result)
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
