/** @odoo-module **/

import { Component, onMounted, proxy } from "@odoo/owl";
import { deserializeDateTime, formatDateTime } from "@web/core/l10n/dates";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

class TradingOverview extends Component {
    static template = "golok_ai_trading_lab_pro.Overview";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.runId = this.props.action?.params?.run_id;
        this.overlays = [
            { key: "ema20", label: _t("EMA 20") },
            { key: "sma20", label: _t("SMA 20") },
            { key: "vwap", label: _t("Session VWAP") },
        ];
        this.state = proxy({ loading: true, error: false, data: null, chart: null, chartLoading: Boolean(this.runId), chartError: false,
            overlay: null });
        this.cards = [
            { key: "instruments", label: _t("Active instruments") },
            { key: "datasets", label: _t("Historical datasets") },
            { key: "candles", label: _t("Stored candles") },
            { key: "runs", label: _t("Research snapshots") },
            { key: "quarantined", label: _t("Quarantined datasets") },
            { key: "experiments", label: _t("Synthetic experiments") },
            { key: "paper_accounts", label: _t("Virtual replay accounts") },
            { key: "successful_syncs", label: _t("Successful historical syncs") },
            { key: "portfolios", label: _t("Synthetic portfolios") },
            { key: "holdouts", label: _t("Sealed evaluations") },
            { key: "candidate_records", label: _t("Fixture candidate records") },
            { key: "performance_reports", label: _t("Synthetic performance reports") },
            { key: "fixture_accounts", label: _t("Prospective fixture accounts") },
            { key: "daily_events", label: _t("Daily research events") },
        ];
        onMounted(() => this.runId ? this.loadChart() : this.refresh());
    }

    async refresh() {
        this.state.loading = true;
        this.state.error = false;
        this.state.chart = null;
        this.state.chartLoading = false;
        this.state.chartError = false;
        this.state.overlay = null;
        try {
            this.state.data = await this.orm.call("golok.lab.run", "overview", []);
        } catch {
            this.state.data = null;
            this.state.error = true;
        } finally {
            this.state.loading = false;
        }
    }

    displayTime(value) {
        return value ? formatDateTime(deserializeDateTime(value), { tz: "Asia/Kolkata" }) : "—";
    }

    async loadChart() {
        this.state.chartLoading = true;
        this.state.chartError = false;
        try {
            const result = await this.orm.call("golok.lab.run", "chart_data", [this.runId || this.state.data.last.id]);
            if (!result?.bars.length) {
                this.state.chartError = true;
                return;
            }
            const rows = result.bars.map(([time, ...values]) => [time, ...values.map(Number)]);
            const series = result.overlays || {};
            const values = Object.values(series).flat().filter((value) => value !== null).map(Number);
            const low = Math.min(...rows.map((row) => row[3]), ...values);
            const high = Math.max(...rows.map((row) => row[2]), ...values);
            const maxVolume = Math.max(...rows.map((row) => row[5])) || 1;
            const position = (value) => high === low ? 50 : (high - value) * 100 / (high - low);
            this.state.chart = {
                high: Math.max(...rows.map((row) => row[2])),
                low: Math.min(...rows.map((row) => row[3])),
                origin: result.origin,
                cutoff: result.cutoff,
                overlays: this.overlays.filter(({ key }) => series[key]?.some((value) => value !== null)),
                first: rows[0][0],
                last: rows.at(-1)[0],
                bars: rows.map(([time, open, upper, lower, close, volume], index) => ({
                    time, up: close >= open, wickTop: position(upper),
                    wickHeight: position(lower) - position(upper),
                    bodyTop: Math.min(position(open), position(close)),
                    bodyHeight: Math.abs(position(open) - position(close)),
                    volume: volume * 100 / maxVolume,
                    overlays: Object.fromEntries(this.overlays.flatMap(({ key }) => {
                        const value = series[key]?.[index];
                        return value == null ? [] : [[key, { value, top: position(Number(value)) }]];
                    })),
                    label: `${this.displayTime(time)} · O ${open} · H ${upper} · L ${lower} · C ${close} · V ${volume}`,
                })),
            };
        } catch {
            this.state.chartError = true;
        } finally {
            this.state.chartLoading = false;
        }
    }

    toggleOverlay(key) {
        this.state.overlay = this.state.overlay === key ? null : key;
    }

    async openList(card) {
        const action = await this.orm.call("golok.lab.run", "overview_card_action", [card.key]);
        return this.action.doAction({ ...action, name: card.label });
    }

    openRun() {
        return this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Research snapshot"),
            res_model: "golok.lab.run",
            res_id: this.state.data.last.id,
            views: [[false, "form"]],
        });
    }

    async openScanner() {
        return this.action.doAction(await this.orm.call("golok.lab.run", "scanner_action", []));
    }
}

registry.category("actions").add("golok_lab.overview", TradingOverview);
