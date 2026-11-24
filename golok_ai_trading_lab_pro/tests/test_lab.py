from datetime import datetime, timedelta

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
