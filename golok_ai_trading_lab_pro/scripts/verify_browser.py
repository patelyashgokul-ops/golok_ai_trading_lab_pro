"""Smoke-test the installed research workflow using headless Edge."""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

MODULE = "golok_ai_trading_lab_pro"
ROOT = Path(__file__).resolve().parent.parent


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
        expect(heading).to_be_visible(timeout=120_000)
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
        expect(page.locator(".o_form_view").get_by_text("RE-01", exact=False)).to_be_visible()
        page.locator(f"[data-menu-xmlid='{MODULE}.menu_overview']").click()
        expect(heading).to_be_visible()
        expect(page.get_by_role("button", name="Stored candles 21")).to_be_visible()
        expect(page.get_by_role("button", name="Research snapshots 1")).to_be_visible()
        expect(page.get_by_text("Synthetic fixture", exact=True)).to_be_visible()
        page.get_by_role("button", name="Refresh").click()
        expect(page.get_by_role("button", name="Open snapshot")).to_be_visible()
        page.screenshot(path=ROOT / "docs/evidence/screenshots/overview-desktop.png")
        page.get_by_role("button", name="Open snapshot").click()
        expect(page.locator(".o_form_view").get_by_text("NO TRADE", exact=True)).to_be_visible()
        print("UI-03 historical research, accurate KPIs, refresh and snapshot drill-down", flush=True)

        page.goto(f"{base_url}/odoo/action-{action_id}")
        page.set_viewport_size({"width": 390, "height": 844})
        expect(heading).to_be_visible()
        expect(page.get_by_text("Synthetic fixture", exact=True)).to_be_visible()
        assert page.locator(".o_golok_overview").evaluate("(el) => el.scrollWidth <= el.clientWidth")
        page.screenshot(path=ROOT / "docs/evidence/screenshots/overview-mobile.png")
        assert not errors, errors
        print("UI-04 mobile viewport without horizontal overflow and no uncaught page errors", flush=True)
        browser.close()


if __name__ == "__main__":
    verify(*sys.argv[1:])
