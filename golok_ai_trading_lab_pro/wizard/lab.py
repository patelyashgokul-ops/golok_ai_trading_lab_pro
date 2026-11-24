from datetime import datetime, timezone

from odoo import _, fields, models
from odoo.exceptions import ValidationError

from ..services import market_data


class ImportCandles(models.TransientModel):
    _name = "golok.lab.import"
    _description = "Import historical candles"

    dataset_id = fields.Many2one("golok.lab.dataset", required=True)
    upload = fields.Binary(required=True, attachment=False, string="CSV")
    filename = fields.Char()

    def action_import(self):
        self.ensure_one()
        self.check_access("read")
        self.dataset_id.check_access("write")
        try:
            if not self.upload or self.upload.size > market_data.MAX_BYTES:
                raise ValueError("Select a CSV of up to 512 KiB.")
            bars = market_data.parse_csv(self.upload.content, as_of=datetime.now(timezone.utc))
        except UnicodeError:
            raise ValidationError(_("CSV must use UTF-8 encoding.")) from None
        except ValueError as exc:
            raise ValidationError(str(exc)) from None
        count = self.dataset_id._import_bars(bars)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": _("%(new)s inserted, %(existing)s already stored.", new=count, existing=len(bars) - count),
                "type": "success",
                "next": {"type": "ir.actions.act_window_close"},
            },
        }


class ResearchWizard(models.TransientModel):
    _name = "golok.lab.research"
    _description = "Run historical research"

    dataset_id = fields.Many2one("golok.lab.dataset", required=True)
    as_of = fields.Datetime(required=True, default=fields.Datetime.now)

    def action_research(self):
        self.ensure_one()
        self.check_access("read")
        run = self.env["golok.lab.run"].create({"dataset_id": self.dataset_id.id, "as_of": self.as_of})
        return {
            "type": "ir.actions.act_window",
            "res_model": run._name,
            "res_id": run.id,
            "view_mode": "form",
            "views": [(False, "form")],
            "target": "current",
        }
