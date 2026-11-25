"""Smoke-test the installed research workflow using headless Edge."""

import base64
import json
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
        expect(page.locator(".o_form_view [name=evidence_contract]")).to_contain_text("r01-research-evidence-1")
        expect(page.locator(".o_form_view [name=evidence_contract]")).to_contain_text("INPUT_UNAVAILABLE")
        print("UI-07 supplemental evidence generated and opened from the research snapshot", flush=True)
        page.goto(f"{base_url}/odoo/action-{action_id}")
        page.get_by_role("button", name="Open snapshot").click()
        page.get_by_role("button", name="Open Stock Chart").click()
        expect(page.get_by_role("heading", name="Stock Research Chart")).to_be_visible()
        expect(page.get_by_text("Calculation cutoff (IST)", exact=False)).to_be_visible()
        expect(page.get_by_role("button", name="Session VWAP")).to_have_count(0)
        page.get_by_role("button", name="EMA 20").click()
        expect(page.locator(".o_golok_overlay_point")).to_have_count(2)
        expect(page.locator(".o_golok_overlay_point").first).to_have_attribute("title", "101")
        page.get_by_role("button", name="SMA 20").click()
        expect(page.locator(".o_golok_overlay_point")).to_have_count(2)
        expect(page.locator(".o_golok_overlay_point").last).to_have_attribute("title", "101")
        page.screenshot(path=EVIDENCE / "screenshots/snapshot-indicators.png")
        print("UI-26 snapshot chart shows the frozen cutoff and independently checked indicator values", flush=True)

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
        page.goto(f"{base_url}/odoo/action-{action_id}")
        page.get_by_role("button", name="Synthetic portfolios 0").click()
        expect(page.locator(".o_list_view")).to_be_visible()
        wizard_id = xml_id("action_portfolio_wizard")
        assert wizard_id
        page.screenshot(path=EVIDENCE / "screenshots/portfolio-list.png")
        assert not errors, errors
        print("UI-10 portfolio KPI reconciles to the company-scoped native portfolio list", flush=True)
        fixture = ROOT / "tests/fixtures/p02"
        spec = json.loads((fixture / "spec.json").read_text())
        revision = call("golok.lab.calendar", "create", {
            "name": "Browser portfolio calendar", "source": "Synthetic fixture", "exchange": "NSE",
            "verification": "fixture", "verified_on": "2024-01-01", "schedule": json.dumps([
                *spec["schedule"], {**spec["schedule"][0], "date": "2024-01-05"}]),
        })
        tariff = call("golok.lab.tariff", "create", {
            "name": "Browser portfolio tariff", "lines": json.dumps(spec["tariffs"]),
        })
        second = call("golok.lab.instrument", "create", {
            "name": "Second Browser Equity", "symbol": "BROWSER2", "exchange": "NSE",
        })
        datasets = []
        for index, asset in enumerate((instrument, second), 1):
            dataset_id = call("golok.lab.dataset", "create", {
                "name": f"Portfolio fixture {index}", "instrument_id": asset, "origin": "synthetic",
                "source": "Browser portfolio public fixture", "interval": "5m", "calendar_id": revision,
            })
            datasets.append(dataset_id)
            for day in (b"2024-01-02", b"2024-01-05"):
                payload = (fixture / "candles.csv").read_bytes().replace(b"2024-01-02", day)
                importer = call("golok.lab.import", "create", {
                    "dataset_id": dataset_id, "upload": base64.b64encode(payload).decode(),
                })
                call("golok.lab.import", "action_import", [importer])
        wizard = call("golok.lab.portfolio.wizard", "create", {
            "dataset_ids": [[6, 0, datasets]], "tariff_id": tariff, "starts": "2024-01-02",
            "ends": "2024-01-02", "strategy": "ST-01", "target_policy": "fixed_4r",
        })
        training = call("golok.lab.portfolio.wizard", "action_run", [wizard])["res_id"]
        page.goto(f"{base_url}/odoo/action-{action_id}")
        summary = page.get_by_role("region", name="Latest synthetic portfolio")
        expect(summary).to_contain_text("49875.96")
        expect(summary).to_contain_text("-124.04")
        page.screenshot(path=EVIDENCE / "screenshots/portfolio-economics.png")
        print("UI-13 closing cash and net portfolio P&L reconcile to the two-instrument synthetic fixture", flush=True)
        page.get_by_role("button", name="Synthetic portfolios 1").click()
        page.locator(".o_list_view .o_data_row").first.click()
        expect(page.get_by_role("heading", name="Synthetic Portfolio Replay")).to_be_visible()
        expect(page.locator(".o_form_view [name=result]")).to_contain_text("SYNTHETIC_SOFTWARE_ONLY")
        expect(page.locator(".o_form_view [name=result]")).to_contain_text("G14")
        page.screenshot(path=EVIDENCE / "screenshots/portfolio-result.png")
        page.get_by_role("tab", name="Frozen Inputs").click()
        expect(page.locator(".o_form_view [name=specification]")).to_contain_text("input_digest")
        assert not errors, errors
        print("UI-11 synthetic replay submitted through Odoo wizard RPC and persisted result, gates and frozen inputs inspected in Edge", flush=True)
        daily_action = xml_id("action_daily_imports")
        page.goto(f"{base_url}/odoo/action-{daily_action}")
        expect(page.locator(".o_list_view")).to_be_visible()
        page.get_by_role("button", name="New", exact=True).first.click()
        expect(page.locator(".o_form_view [name=upload]")).to_be_visible()
        expect(page.locator(".o_form_view [name=corrects_id]")).to_be_visible()
        page.screenshot(path=EVIDENCE / "screenshots/daily-import.png")
        assert not errors, errors
        print("UI-12 end-of-day import list and authorized-file form opened in Edge", flush=True)
        call("golok.lab.portfolio.wizard", "write", [wizard], {
            "training_id": training, "starts": "2024-01-05", "ends": "2024-01-05"})
        call("golok.lab.portfolio.wizard", "action_seal", [wizard])
        page.goto(f"{base_url}/odoo/action-{xml_id('action_holdout')}")
        page.locator(".o_list_view .o_data_row").first.click()
        page.get_by_role("button", name="Consume Final Holdout").click()
        expect(page.get_by_role("heading", name="Synthetic Portfolio Replay")).to_be_visible()
        expect(page.locator(".o_form_view [name=result]")).to_contain_text("SYNTHETIC_SOFTWARE_ONLY")
        print("UI-14 risk-authorized holdout consumed through native form and result displayed", flush=True)
        watch = call("golok.lab.session.watch", "create", {"dataset_id": datasets[0]})
        action = call("golok.lab.session.watch", "action_check_now", [watch])
        assert action["res_model"] == "golok.lab.session.event"
        page.goto(f"{base_url}/odoo/action-{xml_id('action_session_event')}")
        expect(page.locator(".o_list_view")).to_contain_text("NO TRADE")
        expect(page.locator(".o_list_view")).to_contain_text("Fixture-only research")
        page.screenshot(path=EVIDENCE / "screenshots/daily-research-operations.png")
        print("UI-15 persisted fixture-only operational status and NO TRADE visible in native dashboard", flush=True)
        page.locator(".o_list_view .o_data_row").first.click()
        expect(page.get_by_role("heading", name="Daily Research Report")).to_be_visible()
        daily_report = page.locator(".o_form_view [name=daily_report]")
        expect(daily_report).to_contain_text("Recorded phases: 1")
        expect(daily_report).to_contain_text("Realized net (paise): Unavailable")
        expect(daily_report).to_contain_text("Rejected broker requests for this session date: 0")
        page.screenshot(path=EVIDENCE / "screenshots/daily-research-report.png")
        print("UI-27 daily research report reconciles the persisted phases and labels unavailable results", flush=True)
        page.goto(f"{base_url}/odoo/action-{xml_id('action_calendar')}")
        page.locator(".o_list_view").get_by_text("Browser portfolio calendar", exact=True).click()
        page.get_by_role("button", name="Generate Deterministic Fixture").click()
        expect(page.locator(".o_form_view [name=fixture_version]")).to_contain_text("fixture-1")
        expect(page.locator(".o_form_view [name=fixture_digest]")).to_contain_text(re.compile(r"[0-9a-f]{64}"))
        page.screenshot(path=EVIDENCE / "screenshots/generated-fixture.png")
        print("UI-16 deterministic fixture generated and immutable provenance displayed", flush=True)
        generated = call("golok.lab.dataset", "search", [
            ["calendar_id", "=", revision], ["fixture_version", "=", "fixture-1"]])
        assert len(generated) == 1, generated
        timing_wizard = call("golok.lab.portfolio.wizard", "create", {
            "dataset_ids": [[6, 0, generated]], "tariff_id": tariff, "starts": "2024-01-02",
            "ends": "2024-01-02", "strategy": "ST-01",
        })
        call("golok.lab.portfolio.wizard", "action_run_timing_fixture", [timing_wizard])
        page.goto(f"{base_url}/odoo/action-{xml_id('action_portfolio')}")
        page.locator(".o_list_view .o_data_row").first.click()
        expect(page.get_by_role("heading", name="Historical Timing Test on Generated Fixtures")).to_be_visible()
        expect(page.locator(".o_form_view [name=result]")).to_contain_text("HISTORICAL_CONTRACT_FIXTURE_ONLY")
        page.get_by_role("tab", name="Frozen Inputs").click()
        expect(page.locator(".o_form_view [name=specification]")).to_contain_text("generated_fixture_digest")
        assert not errors, errors
        print("UI-17 historical timing fixture persisted and opened with its frozen fingerprint", flush=True)
        page.goto(f"{base_url}/odoo/action-{xml_id('action_portfolio')}")
        page.locator(".o_list_view").get_by_role("row").filter(has_text="ST-01").filter(
            has_not_text="2024-01-05").last.click()
        page.get_by_role("button", name="Calculate Performance").click()
        expect(page.locator(".o_form_view [name=report]")).to_contain_text("p09-performance-2")
        print("UI-18 synthetic performance report persisted with its calculation version", flush=True)
        call("golok.lab.fixture.account", "create", {
            "name": "Browser prospective fixture", "scenario": "target", "tariff_id": tariff})
        page.goto(f"{base_url}/odoo/action-{xml_id('action_fixture_accounts')}")
        page.get_by_text("Browser prospective fixture", exact=True).click()
        page.get_by_role("button", name="Reserve Fixture Order").click()
        page.get_by_role("button", name="Process Fixture Entry").click()
        page.get_by_role("button", name="Process Fixture Exit").click()
        expect(page.locator(".o_form_view [name=order_ids]")).to_contain_text("Closed")
        page.get_by_role("tab", name="Journal (paise)").click()
        expect(page.locator(".o_form_view [name=journal_ids]")).to_contain_text("Closed")
        page.screenshot(path=EVIDENCE / "screenshots/prospective-fixture-journal.png")
        expect(page.locator(".o_form_view [name=mode]")).to_contain_text("Prospective fixture simulation")
        assert not errors, errors
        print("UI-19 fixture-only reservation, entry, exit and journal through native forms", flush=True)
        page.goto(f"{base_url}/odoo/action-{xml_id('action_fixture_risk')}")
        expect(page.locator(".o_list_view")).to_contain_text("Browser prospective fixture")
        expect(page.locator(".o_list_view")).to_contain_text("Remaining Daily Risk")
        expect(page.locator(".o_list_view")).to_contain_text("Daily Realized Net")
        print("UI-20 account risk monitor displays the native remaining budget", flush=True)
        page.goto(f"{base_url}/odoo/action-{xml_id('action_provider_setup')}")
        page.get_by_role("button", name="Check Upstox Readiness").click()
        expect(page.locator(".o_form_view [name=details]")).to_contain_text("read-only historical NSE cash equity")
        expect(page.locator(".o_form_view [name=details]")).to_contain_text("successful receipt (UTC): None")
        page.screenshot(path=EVIDENCE / "screenshots/upstox-readiness.png")
        assert not errors, errors
        print("UI-21 Upstox readiness distinguishes local setup, authorization and historical receipts", flush=True)
        page.get_by_role("button", name="Review Provider Status").click()
        expect(page.locator(".o_form_view [name=details]")).to_contain_text("Upstox historical | historical")
        expect(page.locator(".o_form_view [name=details]")).to_contain_text("Yahoo Finance | unverified")
        expect(page.locator(".o_form_view [name=details]")).to_contain_text("provider-capabilities-1")
        expect(page.locator(".o_form_view [name=details]")).to_contain_text("Current connectivity: Unverified")
        page.screenshot(path=EVIDENCE / "screenshots/provider-status.png")
        print("UI-23 provider status shows source ceilings and current company grants", flush=True)
        page.goto(f"{base_url}/odoo/action-{xml_id('action_research_candidates')}")
        expect(page.locator(".o_list_view")).to_contain_text("Instrument")
        expect(page.locator(".o_list_view")).to_contain_text("Observation At")
        page.screenshot(path=EVIDENCE / "screenshots/fixture-candidate-workspace.png")
        assert not errors, errors
        print("UI-22 fixture candidate workspace exposes instrument and observation provenance", flush=True)
        page.locator(f"[data-menu-xmlid='{MODULE}.menu_import']").click()
        proof_dialog = page.get_by_role("dialog").last
        evidence = proof_dialog.locator("[name=publication_evidence] input")
        evidence.fill("https://example.test/source-evidence")
        evidence.press("Tab")
        expect(proof_dialog.get_by_role("button", name="Verify Comparison Source")).to_be_visible()
        expect(proof_dialog.get_by_role("button", name="Verify Historical Publication")).to_be_visible()
        page.screenshot(path=EVIDENCE / "screenshots/comparison-source-review.png")
        assert not errors, errors
        print("UI-24 comparison verification and replay publication are exposed as separate controls", flush=True)
        proof_dialog.get_by_role("button", name="Cancel").click()
        page.goto(f"{base_url}/odoo/action-{action_id}")
        page.get_by_role("button", name="Prospective fixture accounts 1").click()
        expect(page.locator(".o_list_view .o_data_row")).to_have_count(1)
        expect(page.locator(".o_list_view")).to_contain_text("Browser prospective fixture")
        page.goto(f"{base_url}/odoo/action-{action_id}")
        page.get_by_role("button", name="Daily research events 1").click()
        expect(page.locator(".o_list_view .o_data_row")).to_have_count(1)
        expect(page.locator(".o_list_view")).to_contain_text("Fixture-only research")
        page.screenshot(path=EVIDENCE / "screenshots/reconciled-research-events.png")
        assert not errors, errors
        print("UI-25 prospective account and daily event counts reconcile with scoped lists", flush=True)
        page.goto(f"{base_url}/odoo/action-{xml_id('action_analytics_workspace')}")
        expect(page.get_by_role("heading", name="Market Data API Configuration")).to_be_visible()
        expect(page.get_by_role("textbox", name="Provider")).to_have_value("Offline")
        page.screenshot(path=EVIDENCE / "screenshots/analytics-configuration.png")
        page.get_by_role("button", name="Set or Replace Analytics Token").click()
        secret = page.locator("input[type=password]")
        expect(secret).to_be_visible()
        page.screenshot(path=EVIDENCE / "screenshots/analytics-vault.png")
        authored = "authored-browser-credential"
        secret.fill(authored)
        page.get_by_placeholder("YYYY-MM-DDThh:mm:ss+05:30").fill(
            (datetime.now().astimezone() + timedelta(days=10)).isoformat(timespec="seconds"))
        with page.expect_response(lambda response: response.url.endswith("/golok/analytics/credential")
                                  and response.request.method == "POST") as result:
            page.get_by_role("button", name="Save and Test Connection").click()
        assert result.value.ok and authored not in result.value.text()
        expect(secret).to_have_value("")
        expect(page.get_by_role("status")).to_contain_text("Credential saved in the local Windows vault.")
        expect(page.get_by_text("DISABLED", exact=True)).to_be_visible()
        print("UI-28 masked local credential writes without echo and provider remains disabled", flush=True)
        browser.close()


if __name__ == "__main__":
    verify(*sys.argv[1:])
