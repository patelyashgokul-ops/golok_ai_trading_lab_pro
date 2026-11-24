"""Smoke-test the installed research workflow using headless Edge."""

import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

MODULE = "golok_ai_trading_lab_pro"
ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / os.environ.get("GOLOK_EVIDENCE_DIR", "docs/evidence/p02")


def verify(base_url, database, edge):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=edge, headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(f"{base_url}/web/login?db={database}", wait_until="domcontentloaded")
        page.locator("input[name=login]").fill("admin")
        page.locator("input[name=password]").fill(os.environ["GOLOK_TEST_BROWSER_PASSWORD"])
        page.locator("button[type=submit]").click()
        page.locator(".o_main_navbar").wait_for(timeout=120_000)

        def call(model, method, *args):
            response = page.request.post(
                f"{base_url}/web/dataset/call_kw/{model}/{method}",
                data={"jsonrpc": "2.0", "method": "call", "params": {
                    "model": model, "method": method, "args": list(args), "kwargs": {},
                }},
            ).json()
            if "error" in response:
                raise RuntimeError(response["error"]["data"]["message"])
            return response["result"]

        def xml_id(name):
            return call("ir.model.data", "search_read", [["module", "=", MODULE], ["name", "=", name]], ["res_id"])[0]["res_id"]

        uid = call("res.users", "search", [["login", "=", "admin"]])[0]
        call("res.users", "write", [uid], {"group_ids": [[4, xml_id("group_admin")]]})
        action_id = xml_id("action_overview")
        page.goto(f"{base_url}/odoo/action-{action_id}")
        heading = page.get_by_role("heading", name="Research Overview")
        error_dialog = page.get_by_role("dialog").filter(has=page.get_by_role("heading", name="Oops!"))
        expect(heading.or_(error_dialog)).to_be_visible(timeout=30_000)
        if error_dialog.is_visible():
            error_dialog.get_by_text("See technical details", exact=False).click()
            raise RuntimeError(error_dialog.inner_text())
        expect(page.get_by_text("Create a dataset, import candles", exact=False)).to_be_visible()
        print("UI-01 authenticated OWL dashboard and empty state", flush=True)

        instrument = call("golok.lab.instrument", "create", {"name": "Browser Equity", "symbol": "BROWSER", "exchange": "NSE"})
        call("golok.lab.dataset", "create", {
            "name": "Browser Fixture", "instrument_id": instrument, "origin": "synthetic", "source": "Browser test", "interval": "5m",
        })
        page.locator(f"[data-menu-xmlid='{MODULE}.menu_import']").click()
        dialog = page.get_by_role("dialog")
        expect(dialog.get_by_text("Dataset", exact=True)).to_be_visible()
        dialog.locator(".o_field_many2one input").fill("Browser Fixture")
        page.get_by_text("Browser Fixture", exact=True).last.click()
        start = datetime(2024, 1, 2, 3, 50)
        rows = [
            f"{(start + timedelta(minutes=index * 5)).isoformat()}Z,100,102,99,101,{100 + index}"
            for index in range(21)
        ]
        csv = ("close_time,open,high,low,close,volume\n" + "\n".join(rows)).encode()
        dialog.locator("input[type=file]").set_input_files({"name": "synthetic.csv", "mimeType": "text/csv", "buffer": csv})
        dialog.get_by_role("button", name="Import candles").click()
        expect(page.get_by_text("21 inserted, 0 already stored.")).to_be_visible()
        expect(dialog).to_have_count(0)
        print("UI-02 CSV selected and imported through the Odoo wizard", flush=True)

        page.locator(f"[data-menu-xmlid='{MODULE}.menu_research']").click()
        dialog = page.get_by_role("dialog")
        dialog.locator(".o_field_many2one input").fill("Browser Fixture")
        page.get_by_text("Browser Fixture", exact=True).last.click()
        dialog.get_by_role("button", name="Run research").click()
        expect(page.locator(".o_form_view").get_by_text("NO TRADE", exact=True)).to_be_visible()
        expect(page.locator(".o_form_view [name=evidence_text]")).to_contain_text("RE-01")
        page.locator(f"[data-menu-xmlid='{MODULE}.menu_overview']").click()
        expect(heading).to_be_visible()
        expect(page.get_by_role("button", name="Active instruments 1")).to_be_visible()
        expect(page.get_by_role("button", name="Historical datasets 1")).to_be_visible()
        expect(page.get_by_role("button", name="Stored candles 21")).to_be_visible()
        expect(page.get_by_role("button", name="Research snapshots 1")).to_be_visible()
        expect(page.get_by_text("Synthetic fixture", exact=True)).to_be_visible()
        page.get_by_role("button", name="Refresh").click()
        expect(page.get_by_role("button", name="Open snapshot")).to_be_visible()
        notification = page.locator(".o_notification").filter(has_text="21 inserted")
        if notification.is_visible():
            notification.get_by_role("button").click()
        page.get_by_role("button", name="Show historical chart").click()
        expect(page.get_by_role("img", name="Chronological candlestick chart with volume")).to_be_visible()
        expect(page.locator(".o_golok_plot_col")).to_have_count(21)
        expect(page.locator(".o_golok_plot_col").first).to_have_attribute("title", re.compile(r"O 100.*H 102.*L 99.*C 101"))
        print("UI-06 database-backed OHLC and volume matched the uploaded fixture", flush=True)
        page.screenshot(path=EVIDENCE / "screenshots/overview-desktop.png")
        page.get_by_role("button", name="Open snapshot").click()
        expect(page.locator(".o_form_view").get_by_text("NO TRADE", exact=True)).to_be_visible()
        print("UI-03 historical research, accurate KPIs, refresh and snapshot drill-down", flush=True)
        page.get_by_role("button", name="Run Supplemental Findings").click()
        expect(page.locator(".o_form_view [name=findings]")).to_contain_text("RE-06")
        print("UI-07 supplemental evidence generated and opened from the research snapshot", flush=True)

        page.goto(f"{base_url}/odoo/action-{action_id}")
        page.set_viewport_size({"width": 390, "height": 844})
        expect(heading).to_be_visible()
        expect(page.get_by_text("Synthetic fixture", exact=True)).to_be_visible()
        assert page.locator(".o_golok_overview").evaluate("(el) => el.scrollWidth <= el.clientWidth")
        page.screenshot(path=EVIDENCE / "screenshots/overview-mobile.png")
        assert not errors, errors
        print("UI-04 mobile viewport without horizontal overflow and no uncaught page errors", flush=True)

        dashboard_rpc = "**/web/dataset/call_kw/golok.lab.run/overview**"
        page.route(dashboard_rpc, lambda route: route.fulfill(status=503, body="Unavailable"))
        page.get_by_role("button", name="Refresh").click()
        expect(page.get_by_role("alert")).to_contain_text("Research data is unavailable")
        page.unroute(dashboard_rpc)
        page.get_by_role("button", name="Refresh").click()
        expect(page.get_by_role("button", name="Stored candles 21")).to_be_visible()
        assert not errors, errors
        print("UI-05 refresh gracefully recovered from a failed dashboard RPC", flush=True)
        page.set_viewport_size({"width": 1440, "height": 900})
        page.get_by_role("button", name="Synthetic experiments 0").click()
        expect(page.locator(".o_list_view")).to_be_visible()
        page.goto(f"{base_url}/odoo/action-{action_id}")
        expect(page.get_by_role("button", name="Virtual replay accounts 0")).to_be_visible()
        page.get_by_role("button", name="Virtual replay accounts 0").click()
        expect(page.locator(".o_list_view")).to_be_visible()
        print("UI-08 company experiment and virtual-account cards opened their native lists", flush=True)
        page.goto(f"{base_url}/odoo/action-{action_id}")
        expect(page.get_by_role("button", name="Successful historical syncs 0")).to_be_visible()
        page.get_by_role("button", name="Open Historical Stock Scanner").click()
        expect(page.locator(".o_list_view")).to_contain_text("Browser Equity")
        expect(page.locator(".o_list_view")).to_contain_text("NO TRADE")
        print("UI-09 historical scanner opens with instrument, company data and NO TRADE", flush=True)
        browser.close()


if __name__ == "__main__":
    verify(*sys.argv[1:])
