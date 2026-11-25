"""Intake for independently reviewed Upstox cash-equity publication archives."""

import re
from datetime import datetime, timezone
from hashlib import sha256
from hmac import compare_digest

from odoo import _, fields, models
from odoo.exceptions import AccessError, ValidationError

from ..services import calendar, market_data, upstox


class UpstoxArchive(models.TransientModel):
    _name = "golok.lab.upstox.archive"
    _description = "Import reviewed Upstox publication archive"

    mapping_id = fields.Many2one("golok.lab.mapping", required=True)
    calendar_id = fields.Many2one("golok.lab.calendar", required=True)
    interval = fields.Selection([(value, value) for value in sorted(upstox.INTERVALS)], default="5m", required=True)
    day = fields.Date(required=True)
    upload = fields.Binary(required=True, attachment=False, string="Publication Archive CSV")
    filename = fields.Char()
    evidence_url = fields.Char(required=True, string="Independent Publication Evidence")
    expected_sha256 = fields.Char(required=True, string="Reviewed Archive SHA-256")

    def _read_archive(self, session, now):
        if not self.upload or self.upload.size > market_data.MAX_BYTES:
            raise ValidationError(_("Select a publication CSV of up to 512 KiB."))
        raw = self.upload.content
        digest = sha256(raw).hexdigest()
        expected = (self.expected_sha256 or "").strip().lower()
        if not re.fullmatch(r"[0-9a-f]{64}", expected) or not compare_digest(expected, digest):
            raise ValidationError(_("The CSV does not match the independently reviewed SHA-256."))
        try:
            bars = market_data.parse_csv(raw, as_of=now, temporal=True)
        except (ValueError, UnicodeError) as exc:
            raise ValidationError(_("The publication CSV is invalid: %s", str(exc))) from None
        if [(bar.open_time, bar.close_time) for bar in bars] != session.slots(market_data.INTERVALS[self.interval]):
            raise ValidationError(_("The archive must cover every candle of the selected completed session."))
        published = [bar.available_at for bar in bars]
        if any(left > right for left, right in zip(published, published[1:])):
            raise ValidationError(_("The archive contains out-of-order publication timestamps."))
        return bars, digest

    def action_import_archive(self):
        self.ensure_one()
        self.check_access("read")
        if not self.env.user.has_group("golok_ai_trading_lab_pro.group_admin"):
            raise AccessError(_("A Trading System Administrator is required."))
        company, mapping, revision = self.env.company, self.mapping_id, self.calendar_id
        mapping.check_access("read")
        revision.check_access("read")
        if (mapping.company_id != company or revision.company_id != company or mapping.provider != "upstox"
                or not mapping._covers(self.day, "imported") or not upstox.identity(mapping.exchange, mapping.token, mapping.isin)
                or revision.verification != "reviewed" or revision.exchange != "NSE"):
            raise AccessError(_("Select a reviewed NSE Upstox mapping and calendar in the active company."))
        review = self.env["golok.lab.source.review"]._authorize("upstox", "historical", "analytics_archive")
        if not review.raw_share_ohlcv:
            raise AccessError(_("The review must confirm raw, unadjusted share OHLCV."))
        now = datetime.now(timezone.utc)
        session = revision._sessions().get(self.day)
        if not session or session.kind != "regular" or session.closing > now:
            raise ValidationError(_("Select a completed regular session in the reviewed calendar."))
        bars, digest = self._read_archive(session, now)
        self.env["golok.lab.replay.guard"]._lock(mapping.instrument_id)
        self.env["golok.lab.holdout"]._reject_days(mapping.instrument_id, [self.day], company)
        source = f"Upstox point-in-time {digest} calendar {revision.id} review {review.id}"
        model = self.env["golok.lab.dataset"]
        dataset = model.search([("company_id", "=", company.id), ("instrument_id", "=", mapping.instrument_id.id),
                                ("interval", "=", self.interval), ("source", "=", source)], limit=1)
        with self.env.cr.savepoint():
            if not dataset:
                dataset = model.sudo().with_context({}).create({
                    "company_id": company.id, "name": f"Upstox archive {mapping.symbol} {self.day}",
                    "source": source, "instrument_id": mapping.instrument_id.id, "interval": self.interval,
                    "calendar_id": revision.id, "mapping_id": mapping.id, "origin": "imported",
                    "source_review_id": review.id, "publication_basis": "archive_verified",
                }).with_user(self.env.user)
                dataset._import_bars(bars)
            elif (dataset.mapping_id != mapping or dataset.publication_basis != "archive_verified"
                    or dataset.sudo().source_review_id != review):
                raise AccessError(_("The stored archive has different reviewed lineage."))
            dataset._attest_publication(self.evidence_url, bars)
        return {"type": "ir.actions.act_window", "res_model": dataset._name, "res_id": dataset.id,
                "views": [(False, "form")], "target": "current"}
