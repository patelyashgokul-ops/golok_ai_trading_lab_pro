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
        this.state = proxy({ loading: true, error: false, data: null, chart: null, chartLoading: false, chartError: false });
        this.cards = [
            { key: "instruments", label: _t("Active instruments"), model: "golok.lab.instrument" },
            { key: "datasets", label: _t("Historical datasets"), model: "golok.lab.dataset" },
            { key: "candles", label: _t("Stored candles"), model: "golok.lab.candle" },
            { key: "runs", label: _t("Research snapshots"), model: "golok.lab.run" },
            { key: "quarantined", label: _t("Quarantined datasets"), model: "golok.lab.dataset" },
        ];
        onMounted(() => this.refresh());
    }

    async refresh() {
        this.state.loading = true;
        this.state.error = false;
        this.state.chart = null;
        this.state.chartError = false;
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
            const result = await this.orm.call("golok.lab.run", "chart_data", [this.state.data.last.id]);
            if (!result?.bars.length) {
                this.state.chartError = true;
                return;
            }
            const rows = result.bars.map(([time, ...values]) => [time, ...values.map(Number)]);
            const low = Math.min(...rows.map((row) => row[3]));
            const high = Math.max(...rows.map((row) => row[2]));
            const maxVolume = Math.max(...rows.map((row) => row[5])) || 1;
            const position = (value) => high === low ? 50 : (high - value) * 100 / (high - low);
            this.state.chart = {
                high,
                low,
                first: rows[0][0],
                last: rows.at(-1)[0],
                bars: rows.map(([time, open, upper, lower, close, volume]) => ({
                    time, up: close >= open, wickTop: position(upper),
                    wickHeight: position(lower) - position(upper),
                    bodyTop: Math.min(position(open), position(close)),
                    bodyHeight: Math.abs(position(open) - position(close)),
                    volume: volume * 100 / maxVolume,
                    label: `${this.displayTime(time)} · O ${open} · H ${upper} · L ${lower} · C ${close} · V ${volume}`,
                })),
            };
        } catch {
            this.state.chartError = true;
        } finally {
            this.state.chartLoading = false;
        }
    }

    openList(card) {
        return this.action.doAction({
            type: "ir.actions.act_window",
            name: card.label,
            res_model: card.model,
            views: card.key === "candles" ? [[false, "list"]] : [[false, "list"], [false, "form"]],
            domain: [
                ["company_id", "=", this.state.data.company_id],
                ...(card.key === "instruments" ? [["active", "=", true]] : []),
                ...(card.key === "quarantined" ? [["quarantined", "=", true]] : []),
            ],
        });
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
}

registry.category("actions").add("golok_lab.overview", TradingOverview);
