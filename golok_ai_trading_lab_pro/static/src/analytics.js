/** @odoo-module **/

import { Component, onMounted, proxy, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

class AnalyticsCredential extends Component {
    static template = "golok_ai_trading_lab_pro.AnalyticsCredential";

    setup() {
        this.secretInput = useRef("secret");
        this.expiryInput = useRef("expiry");
        this.state = proxy({ loading: true, banner: "", connection: "", stored: false });
        this.companyId = this.props.action.params.company_id;
        onMounted(() => this.load());
    }

    async load() {
        try {
            const result = await fetch("/golok/analytics/credential?" + new URLSearchParams({ company_id: this.companyId }));
            if (!result.ok) {
                throw new Error();
            }
            const data = await result.json();
            this.csrf = data.csrf;
            this.state.connection = data.connection;
            this.state.stored = data.stored;
        } catch {
            this.state.banner = _t("The credential workspace is unavailable.");
        } finally {
            this.state.loading = false;
        }
    }

    async save() {
        const input = this.secretInput.el;
        const credential = input.value;
        input.value = "";
        this.state.loading = true;
        this.state.banner = "";
        try {
            const result = await fetch("/golok/analytics/credential", {
                method: "POST",
                body: new URLSearchParams({
                    company_id: this.companyId,
                    csrf_token: this.csrf,
                    credential,
                    expiry: this.expiryInput.el.value.trim(),
                }),
            });
            if (!result.ok) {
                throw new Error();
            }
            const data = await result.json();
            this.state.stored = data.stored;
            this.state.connection = data.connection;
            this.state.banner = _t("Credential saved in the local Windows vault.");
        } catch {
            this.state.banner = _t("Credential could not be saved. Check the expiry, your permissions and the local vault.");
        } finally {
            this.state.loading = false;
        }
    }
}

registry.category("actions").add("golok_lab.analytics_secret", AnalyticsCredential);
