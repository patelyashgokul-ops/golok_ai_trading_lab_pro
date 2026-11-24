/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { deserializeDateTime, formatDateTime } from "@web/core/l10n/dates";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

class TradingOverview extends Component {
    static template = "golok_ai_trading_lab_pro.Overview";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ loading: true, error: false, data: null });
        this.cards = [
            { key: "instruments", label: _t("Active instruments"), model: "golok.lab.instrument" },
            { key: "datasets", label: _t("Historical datasets"), model: "golok.lab.dataset" },
            { key: "candles", label: _t("Stored candles"), model: "golok.lab.candle" },
            { key: "runs", label: _t("Research snapshots"), model: "golok.lab.run" },
        ];
        onWillStart(() => this.refresh());
    }

    async refresh() {
        this.state.loading = true;
        this.state.error = false;
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
        return value ? formatDateTime(deserializeDateTime(value)) : "—";
    }

    openList(card) {
        return this.action.doAction({
            type: "ir.actions.act_window",
            name: card.label,
            res_model: card.model,
            views: card.key === "candles" ? [[false, "list"]] : [[false, "list"], [false, "form"]],
            domain: [["company_id", "=", this.state.data.company_id]],
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
