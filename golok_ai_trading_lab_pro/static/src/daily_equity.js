/** @odoo-module **/

import { Component, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";

class DailyEquity extends Component {
    static template = "golok_ai_trading_lab_pro.DailyEquity";

    setup() {
        this.points = this.props.action.params.points;
        onMounted(() => {
            if (this.points.length) {
                this.draw("golok-daily-equity", "cash");
                this.draw("golok-daily-drawdown", "drawdown_percent");
            }
        });
    }

    draw(id, key) {
        const canvas = document.getElementById(id);
        const chart = canvas.getContext("2d");
        const values = this.points.map((row) => Number(row[key]));
        const low = Math.min(...values);
        const high = Math.max(...values);
        const padding = 14;
        const span = canvas.width - 2 * padding;
        const height = canvas.height - 2 * padding;
        const color = getComputedStyle(canvas).color;
        chart.strokeStyle = color;
        chart.fillStyle = color;
        chart.lineWidth = 2;
        const points = values.map((value, index) => [
            values.length === 1 ? canvas.width / 2 : padding + span * index / (values.length - 1),
            high === low ? canvas.height / 2 : padding + height * (high - value) / (high - low),
        ]);
        chart.beginPath();
        chart.moveTo(...points[0]);
        for (const point of points.slice(1)) {
            chart.lineTo(...point);
        }
        chart.stroke();
        for (const point of points) {
            chart.beginPath();
            chart.arc(...point, 3, 0, 2 * Math.PI);
            chart.fill();
        }
    }
}

registry.category("actions").add("golok_lab.daily_equity", DailyEquity);
