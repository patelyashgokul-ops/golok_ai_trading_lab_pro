# Golok AI Trading Lab Pro — P04 development report

## 01 — Executive summary

24 November 2026, Asia/Kolkata. **PAPER TRADING TEST READY for bounded historical synthetic replay only.** P04 delivers one closed-session SmartAPI-shaped fixture through the adapter, mapping/calendar validation, atomic Odoo persistence and audit, plus a historical scanner. Opt-in real historical code was implemented and remains externally unverified. The synthetic replay stops after two consecutive realized losses. The replay journal requires the originally sized capital to match available virtual cash.

## 02 — Actual environment

Verification used local Windows, Odoo 20 Community, PostgreSQL 18.4, Python 3.14.6 and Edge through Playwright. Addon tests ran against disposable loopback databases. The owner’s working database was untouched. The module retains PostgreSQL `btree_gist` for range exclusions. No Git repository was found; the P03 source archive, source manifest and previous report are preserved under the history and evidence directories.

## 03 — Architecture implemented

The historical wizard is administrator-only. It uses a fixed-operation adapter, a company-scoped effective mapping and explicit exchange calendar. The normalizer accepts only a complete, closed grid. The provider timestamp is interpreted as the opening under an explicitly enabled source contract. Candle close is derived from that grid. Local first receipt establishes only application availability; original vendor publication is unknown. The attempt records outcome, receipt and actual coverage. Correct retries insert zero rows; conflicts and incomplete responses do not create accepted observations. The overview exposes successful sync count and a company-scoped historical scanner. Provider-origin datasets remain ineligible for financial replay.

## 04 — Files created and modified

| Area | Paths | Software evidence and scope |
|---|---|---|
| Provider workflow | `models/sync.py`, `models/provider.py`, `services/smartapi.py`, `services/ingestion.py` | Complete single-session fixture, idempotency, negative cases and per-operation worker quotas. Real access pending. |
| Virtual risk | `services/experiments.py`, `models/experiments.py`, `models/paper.py` | Multi-2 loss pause, exact capital match and archived multi-1 records retained. |
| Odoo UI | `views/p04.xml`, `static/src/overview.*`, `models/findings.py` | Native synchronization history, owner wizard, historical scanner and browser regression. |
| Verification | `tests/unit_p04.py`, `tests/test_lab.py`, `scripts/verify_provider_quota.*` | Quote timing, flat/zero-volume indicators, provider ingestion, loss and capital tests, and real quota contention. |

## 05 — Requirement traceability matrix

Original, P02 and P03 identifiers are retained. Updates focus on the reviewed risk, provider, research and browser findings. The complete original wording remains in the governing specification and the previous traceability snapshot remains in history. [Requirements traceability](docs/REQUIREMENTS_TRACEABILITY.md) · [Issue register](docs/P04_REVIEW_ISSUES.md)

## 06 — Research engine status

Seven scoped engine definitions have ORM outputs, including the three P02 findings. Four new engine algorithms and their causal/warm-up behavior were tested in fixtures. None have validated financial outcomes.

| ID | Capability | Implementation and regression | Financial validation |
| --- | --- | --- | --- |
| RE-01 | Technical Analysis | Legacy technical indicators | Not established |
| RE-02 | Fundamental Analysis | Pending | Not established |
| RE-03 | Price Action Analysis | Supplemental six-bar structure | Not established |
| RE-04 | Candlestick Pattern Analysis | Supplemental objective candle geometry | Not established |
| RE-05 | Volume Intelligence | Legacy volume and relative-volume findings | Not established |
| RE-06 | Support and Resistance | Supplemental preceding twenty-bar levels | Not established |
| RE-07 | Breakout Detection | Pending | Not established |
| RE-08 | False Breakout Detection | Pending | Not established |
| RE-09 | Market Trend Analysis | Pending | Not established |
| RE-10 | Sector Performance and Rotation | Pending | Not established |
| RE-11 | Benchmark Index Analysis | Pending | Not established |
| RE-12 | Global Market Context | Pending | Not established |
| RE-13 | Financial News and Event Analysis | Pending | Not established |
| RE-14 | Institutional Activity Proxies | Pending | Not established |
| RE-15 | Historical Pattern Analysis | Pending | Not established |
| RE-16 | Statistical Probability Estimation | Pending | Not established |
| RE-17 | Liquidity Analysis | Pending | Not established |
| RE-18 | Volatility Analysis | Legacy ATR and volatility findings | Not established |
| RE-19 | Momentum Analysis | Supplemental ten-transition momentum | Not established |
| RE-20 | Abnormal Market Activity Detection | Pending | Not established |
| RE-21 | Entry Optimization | Pending | Not established |
| RE-22 | Stop-Loss Optimization | Pending | Not established |
| RE-23 | Profit Target Optimization | Pending | Not established |
| RE-24 | Historical Strategy Performance | Pending | Not established |
| RE-25 | Net Expected Profit and Risk Validation | Pending | Not established |

### Indicator verification

All 19 series were checked against independently specified final outputs on flat, zero-volume data. Existing reference and causal tests were rerun. This does not establish the full indicator-specific reference matrix.

| Indicator | Reference cases executed |
|---|---|
| SMA20, EMA20, RSI14, MACD, ATR14, ADX14 | Flat-series outputs, directional reference/prefix fixtures and existing warm-up assertions |
| VWAP, Opening range, Price gap | Flat and missing-session inputs, explicit session fixtures and multi-session reset |
| Bollinger, Stochastic, Relative volume, ROC, OBV | Flat outputs, zero-range/zero-volume safeguards and existing nonflat references |
| Historical volatility, High/low, Relative strength, Volume spike, Trend slope | Flat outputs and prefix fixture; independent nonflat reference coverage varies by series |

## 07 — Strategy status

| ID | Strategy | Implementation | Financial validation and eligibility |
| --- | --- | --- | --- |
| ST-01 | Opening Range Breakout | multi-2; synthetic Odoo replay with two-loss suspension | Not validated; real-market ineligible |
| ST-02 | VWAP Pullback | Not implemented | Not validated; real-market ineligible |
| ST-03 | VWAP Reclaim | Not implemented | Not validated; real-market ineligible |
| ST-04 | Trend Following | Not implemented | Not validated; real-market ineligible |
| ST-05 | Momentum Continuation | Not implemented | Not validated; real-market ineligible |
| ST-06 | Volume Confirmed Breakout | Not implemented | Not validated; real-market ineligible |
| ST-07 | Support and Resistance Breakout | Not implemented | Not validated; real-market ineligible |
| ST-08 | Mean Reversion | Not implemented | Not validated; real-market ineligible |
| ST-09 | Gap Continuation | Not implemented | Not validated; real-market ineligible |
| ST-10 | Gap Reversal | Not implemented | Not validated; real-market ineligible |
| ST-11 | Multi-Timeframe Trend Confirmation | Not implemented | Not validated; real-market ineligible |
| ST-12 | Relative Strength Momentum | Not implemented | Not validated; real-market ineligible |
| ST-13 | Sector Rotation | Not implemented | Not validated; real-market ineligible |
| ST-14 | Volatility Compression Breakout | Not implemented | Not validated; real-market ineligible |
| ST-15 | Trend Pullback | Not implemented | Not validated; real-market ineligible |
| ST-16 | False Breakout Reversal | Not implemented | Not validated; real-market ineligible |
| ST-17 | Statistical Reversion | Not implemented | Not validated; real-market ineligible |
| ST-18 | ATR-Based Channel Breakout | Not implemented | Not validated; real-market ineligible |
| ST-19 | Momentum Exhaustion | Not implemented | Not validated; real-market ineligible |
| ST-20 | Market Regime Adaptive Strategy | Not implemented | Not validated; real-market ineligible |

## 08 — SmartAPI integration status

The official landing documentation remains access-restricted in the browser. The official SDK source and provider response-structure archive show the REST request and response contracts. Account entitlement, approved egress, fee conditions and permissible storage were unavailable. The code uses a one-session request, an operation-specific local 60-second database quota, HTTPS, bounded response, explicit local opt-in and a process-local token. Three quota races used real independent PostgreSQL transactions. No authentication, historical download, quote or streaming request reached the real provider. The documented offset-less FULL quote example remains unknown for freshness. [Provider response contract](https://smartapi.angelone.in/docs/ResponseStructure) · [Owner actions](docs/OWNER_ACTION_REQUIRED.md)

## 09 — Dashboard development status

| Original area | Scope |
|---|---|
| A Market | Historical counts, source, chart and successful-sync count. Market breadth and live health pending. |
| B Scanner | Company-scoped historical snapshots with instrument and dataset lookup, native filters and pagination. |
| C Opportunities | Existing NO TRADE state. Ranked candidate views pending. |
| D Stock terminal | Real stored OHLC and volume, and supplemental snapshot findings. Wider overlays and controls pending. |
| E Paper | Virtual account and historical replay journal. Prospective marks pending. |
| F Strategies | Synthetic experiment drill-down. Broader strategy dashboards pending. |
| G Risk | Loss/capital enforcement in services. Dedicated portfolio dashboard pending. |
| H Health | Odoo sync attempt audit and owner setup instructions. Quote, WebSocket and long-running health pending. |
| I Daily research | Historical queue and snapshots; automatic daily report pending. |

[Desktop](docs/evidence/p04/release/screenshots/overview-desktop.png) · [Mobile](docs/evidence/p04/release/screenshots/overview-mobile.png)

## 10 — Complete test inventory

122 final passing executions, 0 final failures and 4 named blocked external checks. This includes independently repeated P03 execution. Intermediate install failure is recorded separately.

| Execution ID | Expected check | Final outcome | Evidence |
| --- | --- | --- | --- |
| B-U-01 | test_duplicate_and_reversed_csv | PASSED | baseline/unit.log |
| B-U-02 | test_empty_and_size_limits | PASSED | baseline/unit.log |
| B-U-03 | test_gap_count_and_date_boundary | PASSED | baseline/unit.log |
| B-U-04 | test_invalid_prices_volume_and_timestamps | PASSED | baseline/unit.log |
| B-U-05 | test_utc_normalization_and_exact_prices | PASSED | baseline/unit.log |
| B-U-06 | test_atr_gaps_wilder_smoothing | PASSED | baseline/unit.log |
| B-U-07 | test_reference_values_and_relative_volume_baseline | PASSED | baseline/unit.log |
| B-U-08 | test_warmup_and_no_future_access | PASSED | baseline/unit.log |
| B-U-09 | test_calendar_and_time_availability | PASSED | baseline/unit.log |
| B-U-10 | test_temporal_csv_rejects_early_availability_and_future | PASSED | baseline/unit.log |
| B-U-11 | test_reference_values_and_all_prefixes | PASSED | baseline/unit.log |
| B-U-12 | test_session_reset_and_opening_range | PASSED | baseline/unit.log |
| B-U-13 | test_disabled_transport_and_endpoint_scope | PASSED | baseline/unit.log |
| B-U-14 | test_fixture_auth_history_quote_and_rate_limit | PASSED | baseline/unit.log |
| B-U-15 | test_timeout_sanitizes_transport_error | PASSED | baseline/unit.log |
| B-U-16 | test_token_reuse_and_ineligible_mapping | PASSED | baseline/unit.log |
| B-U-17 | test_breakout_reproducibility_and_stop_first | PASSED | baseline/unit.log |
| B-U-18 | test_tariffs_effective_date_and_risk | PASSED | baseline/unit.log |
| B-U-19 | test_multiple_sessions_stop_at_unknown_calendar_and_reconcile_trades | PASSED | baseline/unit.log |
| B-U-20 | test_split_calendar_has_no_cross_segment_bars | PASSED | baseline/unit.log |
| B-U-21 | test_supplemental_algorithms_warmup_and_preceding_levels | PASSED | baseline/unit.log |
| B-F-01 | test_database_duplicate_constraint | PASSED | baseline/odoo/installation/fresh.log |
| B-F-02 | test_gap_disables_findings | PASSED | baseline/odoo/installation/fresh.log |
| B-F-03 | test_import_retry_and_atomic_conflict | PASSED | baseline/odoo/installation/fresh.log |
| B-F-04 | test_p03_job_worker_and_immutable_corporate_source | PASSED | baseline/odoo/installation/fresh.log |
| B-F-05 | test_p03_mapping_date_scope_and_database_exclusions | PASSED | baseline/odoo/installation/fresh.log |
| B-F-06 | test_p03_supplemental_findings_and_offline_provider_setup | PASSED | baseline/odoo/installation/fresh.log |
| B-F-07 | test_p03_synthetic_workflow_and_reproducible_immutable_results | PASSED | baseline/odoo/installation/fresh.log |
| B-F-08 | test_permissions_and_company_scope | PASSED | baseline/odoo/installation/fresh.log |
| B-F-09 | test_point_in_time_calendar_quarantine_and_chart | PASSED | baseline/odoo/installation/fresh.log |
| B-F-10 | test_research_cutoff_evidence_and_no_trade | PASSED | baseline/odoo/installation/fresh.log |
| B-UO-01 | test_database_duplicate_constraint | PASSED | baseline/odoo/installation/upgrade.log |
| B-UO-02 | test_gap_disables_findings | PASSED | baseline/odoo/installation/upgrade.log |
| B-UO-03 | test_import_retry_and_atomic_conflict | PASSED | baseline/odoo/installation/upgrade.log |
| B-UO-04 | test_p03_job_worker_and_immutable_corporate_source | PASSED | baseline/odoo/installation/upgrade.log |
| B-UO-05 | test_p03_mapping_date_scope_and_database_exclusions | PASSED | baseline/odoo/installation/upgrade.log |
| B-UO-06 | test_p03_supplemental_findings_and_offline_provider_setup | PASSED | baseline/odoo/installation/upgrade.log |
| B-UO-07 | test_p03_synthetic_workflow_and_reproducible_immutable_results | PASSED | baseline/odoo/installation/upgrade.log |
| B-UO-08 | test_permissions_and_company_scope | PASSED | baseline/odoo/installation/upgrade.log |
| B-UO-09 | test_point_in_time_calendar_quarantine_and_chart | PASSED | baseline/odoo/installation/upgrade.log |
| B-UO-10 | test_research_cutoff_evidence_and_no_trade | PASSED | baseline/odoo/installation/upgrade.log |
| B-UI-01 | UI-01 authenticated OWL dashboard and empty state | PASSED | baseline/odoo/browser/edge.log |
| B-UI-02 | UI-02 CSV selected and imported through the Odoo wizard | PASSED | baseline/odoo/browser/edge.log |
| B-UI-03 | UI-06 database-backed OHLC and volume matched the uploaded fixture | PASSED | baseline/odoo/browser/edge.log |
| B-UI-04 | UI-03 historical research, accurate KPIs, refresh and snapshot drill-down | PASSED | baseline/odoo/browser/edge.log |
| B-UI-05 | UI-07 supplemental evidence generated and opened from the research snapshot | PASSED | baseline/odoo/browser/edge.log |
| B-UI-06 | UI-04 mobile viewport without horizontal overflow and no uncaught page errors | PASSED | baseline/odoo/browser/edge.log |
| B-UI-07 | UI-05 refresh gracefully recovered from a failed dashboard RPC | PASSED | baseline/odoo/browser/edge.log |
| B-UI-08 | UI-08 company experiment and virtual-account cards opened their native lists | PASSED | baseline/odoo/browser/edge.log |
| P-U-01 | test_duplicate_and_reversed_csv | PASSED | unit/python.log |
| P-U-02 | test_empty_and_size_limits | PASSED | unit/python.log |
| P-U-03 | test_gap_count_and_date_boundary | PASSED | unit/python.log |
| P-U-04 | test_invalid_prices_volume_and_timestamps | PASSED | unit/python.log |
| P-U-05 | test_utc_normalization_and_exact_prices | PASSED | unit/python.log |
| P-U-06 | test_atr_gaps_wilder_smoothing | PASSED | unit/python.log |
| P-U-07 | test_reference_values_and_relative_volume_baseline | PASSED | unit/python.log |
| P-U-08 | test_warmup_and_no_future_access | PASSED | unit/python.log |
| P-U-09 | test_calendar_and_time_availability | PASSED | unit/python.log |
| P-U-10 | test_temporal_csv_rejects_early_availability_and_future | PASSED | unit/python.log |
| P-U-11 | test_reference_values_and_all_prefixes | PASSED | unit/python.log |
| P-U-12 | test_session_reset_and_opening_range | PASSED | unit/python.log |
| P-U-13 | test_disabled_transport_and_endpoint_scope | PASSED | unit/python.log |
| P-U-14 | test_fixture_auth_history_quote_and_rate_limit | PASSED | unit/python.log |
| P-U-15 | test_timeout_sanitizes_transport_error | PASSED | unit/python.log |
| P-U-16 | test_token_reuse_and_ineligible_mapping | PASSED | unit/python.log |
| P-U-17 | test_breakout_reproducibility_and_stop_first | PASSED | unit/python.log |
| P-U-18 | test_tariffs_effective_date_and_risk | PASSED | unit/python.log |
| P-U-19 | test_multiple_sessions_stop_at_unknown_calendar_and_reconcile_trades | PASSED | unit/python.log |
| P-U-20 | test_split_calendar_has_no_cross_segment_bars | PASSED | unit/python.log |
| P-U-21 | test_supplemental_algorithms_warmup_and_preceding_levels | PASSED | unit/python.log |
| P-U-22 | test_flat_zero_volume_indicator_reference | PASSED | unit/python.log |
| P-U-23 | test_provider_normalization_rejects_future_close_and_wrong_stamp | PASSED | unit/python.log |
| P-U-24 | test_third_losing_session_is_suspended | PASSED | unit/python.log |
| P-U-25 | test_time_and_receipt_are_distinct | PASSED | unit/python.log |
| P-F-01 | test_database_duplicate_constraint | PASSED | release/installation/fresh.log |
| P-F-02 | test_gap_disables_findings | PASSED | release/installation/fresh.log |
| P-F-03 | test_import_retry_and_atomic_conflict | PASSED | release/installation/fresh.log |
| P-F-04 | test_p03_job_worker_and_immutable_corporate_source | PASSED | release/installation/fresh.log |
| P-F-05 | test_p03_mapping_date_scope_and_database_exclusions | PASSED | release/installation/fresh.log |
| P-F-06 | test_p03_supplemental_findings_and_offline_provider_setup | PASSED | release/installation/fresh.log |
| P-F-07 | test_p03_synthetic_workflow_and_reproducible_immutable_results | PASSED | release/installation/fresh.log |
| P-F-08 | test_p04_fixture_sync_atomic_viewable_and_idempotent | PASSED | release/installation/fresh.log |
| P-F-09 | test_permissions_and_company_scope | PASSED | release/installation/fresh.log |
| P-F-10 | test_point_in_time_calendar_quarantine_and_chart | PASSED | release/installation/fresh.log |
| P-F-11 | test_research_cutoff_evidence_and_no_trade | PASSED | release/installation/fresh.log |
| P-UO-01 | test_database_duplicate_constraint | PASSED | release/installation/upgrade.log |
| P-UO-02 | test_gap_disables_findings | PASSED | release/installation/upgrade.log |
| P-UO-03 | test_import_retry_and_atomic_conflict | PASSED | release/installation/upgrade.log |
| P-UO-04 | test_p03_job_worker_and_immutable_corporate_source | PASSED | release/installation/upgrade.log |
| P-UO-05 | test_p03_mapping_date_scope_and_database_exclusions | PASSED | release/installation/upgrade.log |
| P-UO-06 | test_p03_supplemental_findings_and_offline_provider_setup | PASSED | release/installation/upgrade.log |
| P-UO-07 | test_p03_synthetic_workflow_and_reproducible_immutable_results | PASSED | release/installation/upgrade.log |
| P-UO-08 | test_p04_fixture_sync_atomic_viewable_and_idempotent | PASSED | release/installation/upgrade.log |
| P-UO-09 | test_permissions_and_company_scope | PASSED | release/installation/upgrade.log |
| P-UO-10 | test_point_in_time_calendar_quarantine_and_chart | PASSED | release/installation/upgrade.log |
| P-UO-11 | test_research_cutoff_evidence_and_no_trade | PASSED | release/installation/upgrade.log |
| P-UI-01 | UI-01 authenticated OWL dashboard and empty state | PASSED | release/browser/edge.log |
| P-UI-02 | UI-02 CSV selected and imported through the Odoo wizard | PASSED | release/browser/edge.log |
| P-UI-03 | UI-06 database-backed OHLC and volume matched the uploaded fixture | PASSED | release/browser/edge.log |
| P-UI-04 | UI-03 historical research, accurate KPIs, refresh and snapshot drill-down | PASSED | release/browser/edge.log |
| P-UI-05 | UI-07 supplemental evidence generated and opened from the research snapshot | PASSED | release/browser/edge.log |
| P-UI-06 | UI-04 mobile viewport without horizontal overflow and no uncaught page errors | PASSED | release/browser/edge.log |
| P-UI-07 | UI-05 refresh gracefully recovered from a failed dashboard RPC | PASSED | release/browser/edge.log |
| P-UI-08 | UI-08 company experiment and virtual-account cards opened their native lists | PASSED | release/browser/edge.log |
| P-UI-09 | UI-09 historical scanner opens with instrument, company data and NO TRADE | PASSED | release/browser/edge.log |
| P-Q-01 | QUOTA PASS authenticate: two workers, one committed reservation, immediate retry denied | PASSED | quota.log |
| P-Q-02 | QUOTA PASS history: two workers, one committed reservation, immediate retry denied | PASSED | quota.log |
| P-Q-03 | QUOTA PASS quote: two workers, one committed reservation, immediate retry denied | PASSED | quota.log |
| B-C-01 | Identical candle overlap/replay | PASSED | baseline/odoo/security/contention.log |
| B-C-02 | Conflicting candle batch rollback | PASSED | baseline/odoo/security/contention.log |
| B-C-03 | Mapping exclusion | PASSED | baseline/odoo/security/contention.log |
| B-C-04 | Virtual-account posting | PASSED | baseline/odoo/security/contention.log |
| P-C-01 | Identical candle overlap/replay | PASSED | release/security/contention.log |
| P-C-02 | Conflicting candle batch rollback | PASSED | release/security/contention.log |
| P-C-03 | Mapping exclusion | PASSED | release/security/contention.log |
| P-C-04 | Virtual-account posting | PASSED | release/security/contention.log |
| B-R | Archived replay bytes reproduced | PASSED | baseline/replay.json |
| B-S | Archived source inspection | PASSED | baseline/source.log |
| P-R | P04 synthetic replay and ledger conservation | PASSED | replay.json |
| P-S | P04 source inspection | PASSED | source-scan.log |
| P-M | Populated P03 upgrade retention | PASSED | migration/upgrade/retention.log |
| P-P | 50-instrument synthetic ORM benchmark | PASSED | migration/performance/orm.json |
| X-H | Authorized SmartAPI history | BLOCKED | Owner setup and entitlement confirmation |
| X-Q | Authorized quote | BLOCKED | Owner setup and timestamp contract |
| X-W | Real streaming | BLOCKED | Authorization and streaming implementation |
| X-F | Actual historical financial experiment | BLOCKED | Approved as-of dataset and applicable tariffs |

## 11 — Actual test execution evidence

The command inventory records exact repeatable commands, expected scope, measured durations where retained, exit codes and artifacts. The archived P03 synthetic JSON matched its previously captured artifact. The populated upgrade retained 494 XML IDs plus the original instrument, dataset, candle and snapshot hashes. [Commands](docs/evidence/p04/COMMANDS.md) · [Migration](docs/evidence/p04/migration/upgrade/retention.log)

## 12 — Business invariant verification

| ID | Requirement | Status | Path | Test | Evidence | Remaining scope |
|---|---|---|---|---|---|---|
| INV-01 | No real broker order execution | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-02 | No mandatory paid AI dependency | COMPLETE | `__manifest__.py`, `services/` | U01–U08 | `docs/evidence/tests/unit.log` | — |
| INV-03 | No GPU dependency | COMPLETE | `__manifest__.py`, `services/` | U01–U08 | `docs/evidence/tests/unit.log` | — |
| INV-04 | No fabricated live market data | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-05 | No actionable signal from stale required data | GUARD_ONLY | `services/research.py`, `models/lab.py` | O05–O06 | `docs/evidence/installation/{fresh,upgrade}.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-06 | No look-ahead bias | PARTIAL | `services/research.py`, `models/lab.py` | U07, O05 | `docs/evidence/tests/unit.log` | Close-time cutoff proven by snapshot assertion if ORM passes. Point-in-time vendor availability, survivorship and future execution tests remain. |
| INV-07 | No future information in historical decisions | PARTIAL | `services/research.py`, `models/lab.py` | U07, O05 | `docs/evidence/tests/unit.log` | Close-time cutoff proven by snapshot assertion if ORM passes. Point-in-time vendor availability, survivorship and future execution tests remain. |
| INV-08 | No duplicate market data records | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03–O04, O08 | `docs/evidence/installation/{fresh,upgrade}.log`, `docs/evidence/security/contention.log` | — |
| INV-09 | No duplicate paper-trade execution | PARTIAL | See P03 criterion or related service | See P03 execution inventory | docs/evidence/p03/COMMANDS.md | Historical journal fill idempotency verified under actual overlap; prospective lifecycle pending. |
| INV-10 | No misleading profit guarantees | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-11 | No uncalibrated score represented as probability | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-12 | No unauthorized broker credential exposure | PARTIAL | See P04 issue inventory | P-U; P-O; P-UI | docs/evidence/p04/COMMANDS.md | Process-local broker token, server-side environment permissions and sanitized statuses; broker session not exercised. |
| INV-13 | No strategy promotion without validation | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-14 | No retrospective performance manipulation | PARTIAL | `services/research.py`, `models/lab.py` | O05, O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Snapshot input hashes and role-level immutability exist. Add experiment parameters, amendments and prospective outcomes. |
| INV-15 | No silent synthetic-data substitution | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-16 | No ignoring material transaction costs in net returns | PARTIAL | See P03 criterion or related service | See P03 execution inventory | docs/evidence/p03/COMMANDS.md | Hypothetical synthetic fees verified; actual fee reconciliation unavailable. |
| INV-17 | No invalid position sizing | PARTIAL | See P03 criterion or related service | See P03 execution inventory | docs/evidence/p03/COMMANDS.md | Synthetic cash sizing and independent risk veto exercised. |
| INV-18 | No cross-company unauthorized access | COMPLETE | `security/ir.access.csv`, `models/lab.py` | O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Add regression checks for future features and independent API calls. |
| INV-19 | No risk veto overridden by signal score | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-20 | No forced daily trading recommendation | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-21 | No experimental strategy presented as validated | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-22 | No real account capital allocation | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-23 | No unbounded background processing | COMPLETE | See P04 issue inventory | P-U; P-O; P-UI | docs/evidence/p04/COMMANDS.md | Existing queue remains bounded; provider synchronization is one session and the adapter has capped response and quotas. |
| INV-24 | No paper profit represented as real profit | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-25 | No test marked PASSED without execution evidence | COMPLETE | `DEVELOPMENT_REPORT.md` | D01 | Sections 10–15 and 22 | No financial performance or production readiness claimed. |
| INV-26 | No unsupported market data entitlement bypass | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-27 | No missing required data treated as positive evidence | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-28 | No historical signal deletion to hide losses | PARTIAL | `services/research.py`, `models/lab.py` | O05, O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Snapshot input hashes and role-level immutability exist. Add experiment parameters, amendments and prospective outcomes. |
| INV-29 | No dashboard KPI without a defined data source | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-30 | No production-readiness claim with unresolved critical blockers | COMPLETE | `DEVELOPMENT_REPORT.md` | D01 | Sections 10–15 and 22 | No financial performance or production readiness claimed. |

## 13 — Acceptance criteria verification

Original and earlier milestone statuses retain their documented scope. P04 PASSED applies to the exact software behavior evidenced in its row. External integration and financial validation have separate outcomes.

| ID | Requirement | Status | Path | Test | Evidence | Remaining scope |
|---|---|---|---|---|---|---|
| AC-001 | Odoo 20 Community compatibility verified | COMPLETE | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| AC-002 | Fresh installation successful | COMPLETE | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| AC-003 | Module upgrades safely | COMPLETE | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| AC-004 | Zero mandatory paid AI APIs | COMPLETE | `__manifest__.py`, `services/` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Runtime manifest and expanded standard-library services verified. |
| AC-005 | CPU-only operation | COMPLETE | `__manifest__.py`, `services/` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | CPU-only synthetic ORM benchmark. |
| AC-006 | 16 GB hardware optimization measured | PARTIAL | `scripts/measure_services.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | 50 instruments measured in P02. Larger workloads pending. |
| AC-007 | Secure provider configuration | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Opt-in environment configuration tested offline; account authorization pending. |
| AC-008 | Instrument master synchronization | NOT_STARTED | `models/lab.py` | — | Manual registration only | Add verified provider instrument master sync and token mapping. |
| AC-009 | Historical market data ingestion | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Calendar-aware CSV implemented, broker history verified in fixtures. |
| AC-010 | Authorized live market data integration | BLOCKED | — | B01 | Decision and sources in §08 | Verify account terms, static egress and authorized credentials. Implement a read-only adapter. |
| AC-011 | Market data freshness enforcement | PARTIAL | `services/research.py`, `models/lab.py` | O05–O06 | `docs/evidence/installation/{fresh,upgrade}.log` | NO TRADE blocks actionable historical signals. Implement live freshness or expiry gates before enabling actionable signals. |
| AC-012 | Duplicate-data prevention | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03–O04, O08 | `docs/evidence/installation/{fresh,upgrade}.log`, `docs/evidence/security/contention.log` | — |
| AC-013 | Historical data provenance | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| AC-014 | Correct indicator calculations | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | 19 causal series implemented. Full independent reference verification pending. |
| AC-015 | Research engine interface operational | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Version 2 contract implemented for three results. |
| AC-016 | Applicable research capabilities functional | PARTIAL | See P04 issue inventory | P-U; P-O; P-UI | docs/evidence/p04/COMMANDS.md | Seven scoped legacy and supplemental engines. P04 standalone and ORM rerun. |
| AC-017 | Versioned strategy framework | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | ST-01 version and code hashes; general strategy lifecycle pending. |
| AC-018 | Market regime detection | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-019 | Explainable master decision engine | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | NO TRADE with temporal and quarantine gates. Master gates pending. |
| AC-020 | Transparent quality scoring | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-021 | Risk veto enforcement | PARTIAL | See P04 issue inventory | P-U; P-O; P-UI | docs/evidence/p04/COMMANDS.md | Fee-aware veto and two-loss suspension exercised. Aggregate risk pending. |
| AC-022 | Transaction cost calculation | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Effective-dated cost engine works with documented hypothetical tariffs. |
| AC-023 | Expected net return calculation | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Synthetic net results v1. Validated evidence and calibration remain. |
| AC-024 | Position sizing validation | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Fee-aware sizing and stop risk verified for the synthetic slice. |
| AC-025 | Signal freshness and expiry | PARTIAL | `services/research.py`, `models/lab.py` | O05–O06 | `docs/evidence/installation/{fresh,upgrade}.log` | NO TRADE blocks actionable historical signals. Implement live freshness or expiry gates before enabling actionable signals. |
| AC-026 | Historical backtesting | PARTIAL | See P04 issue inventory | P-U; P-O; P-UI | docs/evidence/p04/COMMANDS.md | Single-instrument synthetic multi-session replay and frozen cash enforcement. Authorized financial replay pending. |
| AC-027 | Look-ahead bias prevention | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Cutoff, prefix invariance and next-opening rules tested; real data lineage pending. |
| AC-028 | Out-of-sample validation | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-029 | Walk-forward testing | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-030 | Reproducible research experiments | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Synthetic code and data hashes verified. Holdout workflow pending. |
| AC-031 | Automatic paper trading | PARTIAL | See P03 criterion or related service | See P03 execution inventory | docs/evidence/p03/COMMANDS.md | Virtual historical posting exists; prospective paper execution disabled. |
| AC-032 | Virtual cash integrity | PARTIAL | See P03 criterion or related service | See P03 execution inventory | docs/evidence/p03/COMMANDS.md | Virtual historical cash and reservations reconcile atomically. |
| AC-033 | Paper execution idempotency | PARTIAL | See P03 criterion or related service | See P03 execution inventory | docs/evidence/p03/COMMANDS.md | Historical batch idempotency verified with independent PostgreSQL transactions. |
| AC-034 | Paper portfolio reporting | PARTIAL | See P03 criterion or related service | See P03 execution inventory | docs/evidence/p03/COMMANDS.md | Persisted virtual accounts and journal. Portfolio/equity reporting incomplete. |
| AC-035 | Strategy performance tracking | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-036 | Recommendation monitoring | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-037 | Automatic research scheduling | PARTIAL | See P03 criterion or related service | See P03 execution inventory | docs/evidence/p03/COMMANDS.md | Bounded historical Odoo queue and inactive cron; daily/market scheduler absent. |
| AC-038 | Scheduler concurrency protection | PARTIAL | See P03 criterion or related service | See P03 execution inventory | docs/evidence/p03/COMMANDS.md | Skip-locked claim implemented; independent job claim testing pending. |
| AC-039 | Premium dashboard operational | PARTIAL | `static/src/`, `views/lab.xml`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Native historical plot and company KPI additions. Full dashboards A–I incomplete. |
| AC-040 | Dashboard KPI correctness | COMPLETE | `static/src/`, `views/lab.xml`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Current overview KPI/fixture chart values verified in Edge. |
| AC-041 | Real browser UI verified | PARTIAL | See P04 issue inventory | P-U; P-O; P-UI | docs/evidence/p04/COMMANDS.md | Nine Edge checks including historical scanner; full dashboard verification pending. |
| AC-042 | Security permissions verified | COMPLETE | `security/ir.access.csv`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Current ACLs reverified, including calendar administration and forged research creation. |
| AC-043 | Company isolation verified | COMPLETE | `security/ir.access.csv`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Company isolation regression passed. |
| AC-044 | Credential redaction verified | PARTIAL | `__manifest__.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Credential redaction checked with offline failure fixtures. No actual credential run. |
| AC-045 | Recovery behavior verified | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Independent conflicting imports and retry verified. |
| AC-046 | No real-order functionality | COMPLETE | `__manifest__.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Mandatory prohibition verified by runtime endpoint rejection and source scan. |
| AC-047 | NO TRADE behavior verified | COMPLETE | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | NO TRADE verified in ORM and browser. |
| AC-048 | No fabricated performance results | COMPLETE | `DEVELOPMENT_REPORT.md` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Only synthetic correctness evidence reported. |
| AC-049 | Complete setup and user documentation | PARTIAL | `README.md` | D01 | README and §21 | Document setup for functionalities as they are implemented. |
| AC-050 | Evidence-backed development report generated | COMPLETE | `DEVELOPMENT_REPORT.md` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | P02 handoff and manifest verified. |

| ID | Requirement | Status | Scope | Evidence |
|---|---|---|---|---|
| P02-AC-001 | P01 baseline preserved | PASSED | Migration and populated retention | verify_p01_upgrade.ps1; upgrade/retention.log |
| P02-AC-002 | Previous defects independently revalidated | PASSED | P01 reruns and P02 browser/ORM regression | baseline/audit.log; baseline/browser.log |
| P02-AC-003 | Traceability semantics corrected | PASSED | Semantic guards, prohibitions and optional technologies separated | REQUIREMENTS_TRACEABILITY.md |
| P02-AC-004 | Evidence integrity verified | PASSED | P01 and P02 manifest verification | baseline/audit.log; manifest.sha256 |
| P02-AC-005 | Source checkpoint established | PASSED | Verified recovery archive | history/P01-source.zip; baseline/source.sha256 |
| P02-AC-006 | Exchange calendar service implemented | PASSED | Explicit versioned NSE and BSE calendar records | services/calendar.py; unit/python.log |
| P02-AC-007 | Session-aware candle validation | PASSED | Grid mismatch, closed days, cutoffs and missing observations | installation/fresh.log; unit/python.log |
| P02-AC-008 | Point-in-time data contract | PASSED | Opening, closing, publication, ingestion and cutoff semantics | models/lab.py; installation/fresh.log |
| P02-AC-009 | Instrument reference mapping integrity | PASSED | Effective-dated identity, P03 overlap race and company isolation verified. | docs/evidence/p03/COMMANDS.md |
| P02-AC-010 | Data quality eligibility enforcement | PARTIAL | Temporal and quarantine guards; source verification and unified eligibility incomplete | models/lab.py; installation/fresh.log |
| P02-AC-011 | Synthetic-data isolation | PASSED | Fixtures have explicit origin and calendar constraints | models/lab.py; unit/python.log |
| P02-AC-012 | Read-only provider interface | PASSED | Fixed REST allowlist and disabled default transport | services/smartapi.py; unit/python.log |
| P02-AC-013 | SmartAPI adapter fixture tests | PASSED | Deterministic fixture login, history and quote | tests/unit_p02.py; unit/python.log |
| P02-AC-014 | Provider timeout and rate-limit protection | PASSED | Client-local timeout, pacing and response limits | services/smartapi.py; unit/python.log |
| P02-AC-015 | Secure credential handling | PASSED | Environment and process-local tokens with sanitized fixture failures | services/smartapi.py; unit/python.log |
| P02-AC-016 | Live verification correctly classified | PASSED | No authenticated live request made | SMARTAPI_SETUP.md |
| P02-AC-017 | Technical indicator mathematical verification | PARTIAL | All 19 indicators implemented; full independent numerical cross-verification is incomplete | INDICATOR_FORMULAS.md; unit/python.log |
| P02-AC-018 | Indicator prefix invariance | PASSED | All 19 series checked at five prefixes of a reference fixture | tests/unit_p02.py; unit/python.log |
| P02-AC-019 | Versioned research engine contract | PARTIAL | Version 2 contract covers three ORM engines. Other engines remain pending. | models/lab.py; installation/fresh.log |
| P02-AC-020 | Effective-dated transaction costs | PASSED | Decimal, per-side and effective-dated tariffs with hypothetical inputs | services/simulation.py; unit/python.log |
| P02-AC-021 | Fee-aware position sizing | PASSED | Fee-adjusted capital, risk and liquidity constraints | services/simulation.py; unit/python.log |
| P02-AC-022 | Independent risk veto | PASSED | Independent net reward-to-risk veto | services/simulation.py; unit/python.log |
| P02-AC-023 | Versioned strategy framework | PARTIAL | Persistent ST-01 synthetic strategy version added. Full version workflow and promotion pending. | docs/evidence/p03/COMMANDS.md |
| P02-AC-024 | ST-01 research strategy implementation | PASSED | Single-instrument synthetic ST-01 runs in Odoo across regular sessions. | docs/evidence/p03/COMMANDS.md |
| P02-AC-025 | Conservative historical simulation | PASSED | Later openings, stop-first ambiguity and conservative exits in one-session replay | services/backtest.py; unit/python.log |
| P02-AC-026 | Backtest reproducibility | PASSED | Frozen parameters, code and dataset digests; deterministic replay | services/backtest.py; backtesting/synthetic.json |
| P02-AC-027 | Holdout isolation | PARTIAL | Partition label exists; temporal split and one-time holdout enforcement are missing | docs/BACKTEST_EXECUTION_POLICY.md |
| P02-AC-028 | Financial performance provenance | PASSED | Synthetic provenance is explicit; no validated-market sample or reported market performance | backtesting/synthetic.json |
| P02-AC-029 | Structured NO TRADE enforcement | PARTIAL | Existing NO TRADE and individual reasons; fourteen-gate pipeline incomplete | models/lab.py; installation/fresh.log |
| P02-AC-030 | No actionable real-market recommendation leakage | PASSED | Historical/fixture-only decisions, no executable path | unit/python.log; security/source-scan.log |
| P02-AC-031 | Virtual ledger integrity | PASSED | Scoped historical-only virtual ledger reconciles exactly. | docs/evidence/p03/COMMANDS.md |
| P02-AC-032 | Virtual execution idempotency | PASSED | Posting idempotency verified under overlapping PostgreSQL transactions. | docs/evidence/p03/COMMANDS.md |
| P02-AC-033 | Premium OWL dashboard improvements | PARTIAL | Overview, chart, quarantine and data provenance; remaining terminal areas incomplete | static/src; browser/edge.log |
| P02-AC-034 | Actual database-backed chart values | PASSED | Actual bounded chart values tested through the browser and ORM | browser/edge.log; installation/fresh.log |
| P02-AC-035 | Authorized dashboard drill-downs | PASSED | Company and permission checked chart and existing native drill-down | browser/edge.log; installation/fresh.log |
| P02-AC-036 | Real browser verification | PARTIAL | Six real Edge checks passed; requested full theme, pagination and stale coverage remains | browser/edge.log |
| P02-AC-037 | End-to-end performance measurement | PASSED | Measured 50 instruments through ORM import and research | performance/orm.json |
| P02-AC-038 | Resource-bound execution | PARTIAL | Core paths bounded; job constraints and configured deadlines pending | services; performance/orm.json |
| P02-AC-039 | Complete security regression | PARTIAL | Targeted ACL, company, forged create, quarantine and endpoint checks; complete program pending | installation/fresh.log; unit/python.log |
| P02-AC-040 | Updated evidence-backed development report | PASSED | Updated 22-section handoff, matrices and validated checksums | DEVELOPMENT_REPORT.md; manifest.sha256 |

| ID | Requirement | Status | Scope | Evidence |
|---|---|---|---|---|
| P03-AC-001 | P01 and P02 source preservation | PASSED | Verified P02 source ZIP; P01 source and evidence retained. | baseline/source.sha256 |
| P03-AC-002 | Previous test regression executed | PASSED | Archived P02 standalone, ORM, contention and Edge suites executed; P02 suite includes P01 regressions. | baseline/p02-retest |
| P03-AC-003 | Evidence manifests verified | PASSED | 10 P01 and 22 P02 evidence hashes, P02 source and final P03 evidence rechecked. | baseline/audit.log |
| P03-AC-004 | Original traceability reconciled | PARTIAL | Selected implementation rows updated; unimplemented requirements and inherited IDs retained. | docs/REQUIREMENTS_TRACEABILITY.md |
| P03-AC-005 | Execution counts independently reconciled | PARTIAL | P03 counts reconstructed per execution; P02 original totals retained as historical with a fresh baseline run. | COMMANDS.md |
| P03-AC-006 | Persistent instrument mapping | PASSED | Versioned company mapping with native search and mapped datasets. | release/installation/fresh.log |
| P03-AC-007 | Effective-date overlap prevention | PASSED | Database token, symbol and identity range guards; independently overlapping tokens rejected. | release/security/contention.log |
| P03-AC-008 | Corporate action provenance | PASSED | Immutable effective date, publication time, source/revision and split ratio. | release/installation/fresh.log |
| P03-AC-009 | Point-in-time universe integrity | BLOCKED | Historical membership and corporate adjustment source history unavailable. | docs/CORPORATE_ACTION_POLICY.md |
| P03-AC-010 | Expanded exchange calendar | PASSED | Split windows, pre/post markers, truncated slots, UTC normalization and cross-segment rejection. | unit/python.log |
| P03-AC-011 | Secure operational provider configuration | PASSED | Admin-only diagnostics, environment credentials and offline default. | release/installation/fresh.log |
| P03-AC-012 | Real read-only transport implementation | PARTIAL | Fixed read-only REST transport exists; authenticated real transport not exercised. | baseline/unit.log; models/provider.py |
| P03-AC-013 | Provider-to-ORM ingestion | NOT_RUN | An authorized provider-to-ORM market data pipeline remains unimplemented. | docs/MARKET_DATA_SOURCES.md |
| P03-AC-014 | Shared provider rate limiting | PARTIAL | Database-shared diagnostic authentication pacing only; no unified limiter for all market requests. | models/provider.py |
| P03-AC-015 | Historical integration verification | BLOCKED | No authorized historical SmartAPI request. | docs/PROVIDER_OPERATIONS.md |
| P03-AC-016 | Live quote verification | BLOCKED | No authorized real quote. | docs/PROVIDER_OPERATIONS.md |
| P03-AC-017 | Streaming integration verification | BLOCKED | No authorized WebSocket. | docs/PROVIDER_OPERATIONS.md |
| P03-AC-018 | Provider failure recovery | PARTIAL | Existing sanitized timeouts and local pacing; automated credential or streaming recovery absent. | unit/python.log |
| P03-AC-019 | Market data freshness enforcement | PARTIAL | Historical cutoff, session validation and NO TRADE; live market freshness contract absent. | release/installation/fresh.log |
| P03-AC-020 | Complete indicator reference tests | PARTIAL | 19 existing series rerun; full independent per-indicator boundary matrix incomplete. | unit/python.log |
| P03-AC-021 | Versioned research registry | PARTIAL | Versioned four-engine supplemental registry; complete 25-engine framework pending. | services/research_v3.py |
| P03-AC-022 | OHLCV-supported research engines | PARTIAL | Four additional OHLCV engines exercised; broader requested engine set remains partial. | unit/python.log |
| P03-AC-023 | Research evidence persistence | PASSED | Immutable supplemental outputs with original digest, cutoff and duration. | release/installation/fresh.log |
| P03-AC-024 | Market regime classification | NOT_RUN | No market-wide regime classifier. | docs/RESEARCH_ENGINE_CATALOG.md |
| P03-AC-025 | Persistent tariff configuration | PASSED | Risk Manager company-scoped immutable hypothetical tariff revisions. | release/installation/fresh.log |
| P03-AC-026 | Verified tariff provenance | BLOCKED | Verified tariff sourcing and reconciled contract-note data unavailable. | docs/TRANSACTION_COST_MODEL.md |
| P03-AC-027 | Fee-aware risk calculation | PASSED | Reuses existing Decimal sizing and risk veto in replay. | unit/python.log |
| P03-AC-028 | Aggregate portfolio risk enforcement | NOT_RUN | Aggregate portfolio risk and concentration limits remain open. | docs/RISK_POLICY.md |
| P03-AC-029 | Persistent strategy registry | PARTIAL | Persistent ST-01 research version; promotion/approval and lifecycle incomplete. | views/p03.xml |
| P03-AC-030 | Multi-session ST-01 | PASSED | Two regular synthetic sessions replayed with sequential virtual cash. | backtesting/synthetic-replay-ledger.json |
| P03-AC-031 | Odoo backtesting workflow | PASSED | Native experiment wizard, result form and dashboard link working in tested scope. | release/installation/fresh.log; release/browser/edge.log |
| P03-AC-032 | Immutable experiment specification | PARTIAL | Data, strategy, tariff, risk and calendar fingerprints; universe, benchmarks and sealed splits pending. | models/experiments.py |
| P03-AC-033 | Multi-instrument historical replay | NOT_RUN | Only a single instrument can be replayed. | docs/VALIDATION_PROTOCOL.md |
| P03-AC-034 | Conservative execution verification | PASSED | Rejects unavailable opens and stops at unknown calendar; stop-first conservative fixture. | unit/python.log |
| P03-AC-035 | Financial metrics correctness | PARTIAL | Trade counts, net, costs, turnover and closing-equity drawdown; excursion/risk ratios not verified. | backtesting/synthetic-replay-ledger.json |
| P03-AC-036 | Holdout isolation | NOT_RUN | No sealed holdout consumption control. | docs/VALIDATION_PROTOCOL.md |
| P03-AC-037 | Walk-forward infrastructure | NOT_RUN | No walk-forward experiment source. | docs/VALIDATION_PROTOCOL.md |
| P03-AC-038 | Financial validation provenance | BLOCKED | No authorized dataset or verified tariff suitable for financial validation. | docs/VALIDATION_PROTOCOL.md |
| P03-AC-039 | Master decision gate enforcement | PARTIAL | NO TRADE and synthetic mode enforced; fourteen-gate engine incomplete. | release/installation/fresh.log |
| P03-AC-040 | Research scoring transparency | NOT_RUN | No ranking or calibrated score. | docs/RESEARCH_ENGINE_CATALOG.md |
| P03-AC-041 | Atomic virtual cash ledger | PASSED | Historical virtual cash and events are atomic and balanced. | release/security/contention.log |
| P03-AC-042 | Reservation reconciliation | PASSED | Independent cash, reservation and quantity reconciliation re-executed. | unit/python.log |
| P03-AC-043 | Virtual position integrity | PARTIAL | Closed replay positions reconcile; persistent open and partial lifecycle absent. | docs/PAPER_LEDGER_INVARIANTS.md |
| P03-AC-044 | Fill idempotency | PASSED | Database unique batch, event identity and retry verified. | release/security/contention.log |
| P03-AC-045 | Paper lifecycle verification | PARTIAL | Reserve/buy/close workflow for complete historical replay; prospective lifecycle excluded. | release/installation/fresh.log |
| P03-AC-046 | Virtual ledger concurrency | PASSED | Actual overlap and idempotent retry produced precisely one reconciled batch. | release/security/contention.log |
| P03-AC-047 | Paper restart recovery | NOT_RUN | No live worker restart scenario. | docs/PAPER_LEDGER_INVARIANTS.md |
| P03-AC-048 | Historical/prospective separation | PARTIAL | Historical isolation enforced; no prospective implementation to verify. | docs/PAPER_LEDGER_INVARIANTS.md |
| P03-AC-049 | Persistent background jobs | PASSED | Persistent historical queue and requester identity with bounded worker verified. | release/installation/fresh.log |
| P03-AC-050 | Scheduler concurrency protection | PARTIAL | Skip-locked scheduler with no separate cross-worker job test. | models/jobs.py |
| P03-AC-051 | Daily research orchestration | NOT_RUN | No exchange-triggered daily coordination. | docs/BACKGROUND_JOBS.md |
| P03-AC-052 | Functional stock scanner | PARTIAL | Searchable mapping directory and native lists; full stock scanner pending. | views/p03.xml |
| P03-AC-053 | Advanced stock research terminal | PARTIAL | Chart and supplemental drill-down work; overlays and expanded terminal controls pending. | release/browser/edge.log |
| P03-AC-054 | Strategy dashboard | PARTIAL | Native synthetic experiments and verified dashboard drill-down. Strategy metrics/dashboard incomplete. | release/browser/edge.log |
| P03-AC-055 | Paper portfolio dashboard | PARTIAL | Native virtual accounts and replay journal, plus one overview tile. Prospective metrics absent. | release/browser/edge.log |
| P03-AC-056 | Risk control dashboard | NOT_RUN | No dedicated portfolio risk dashboard. | docs/RISK_POLICY.md |
| P03-AC-057 | Provider health dashboard | PARTIAL | Offline administrator diagnostics, no live health dashboard. | release/installation/fresh.log |
| P03-AC-058 | Daily research report | NOT_RUN | No daily aggregation view. | docs/BACKGROUND_JOBS.md |
| P03-AC-059 | Dashboard KPI reconciliation | PASSED | Company-scoped card and chart values reconciled in browser and ORM. | release/browser/edge.log |
| P03-AC-060 | Real browser verification | PASSED | Eight real Edge assertions, including mobile and RPC recovery. | release/browser/edge.log |
| P03-AC-061 | End-to-end performance | PASSED | 50 instruments, 3,750 candles, 361 SQL statements measured. | migration/performance/orm.json |
| P03-AC-062 | Resource pressure handling | PARTIAL | Bounded reads and job batches; no operating system pressure/failure injection suite. | docs/PERFORMANCE_LIMITS.md |
| P03-AC-063 | Security regression | PARTIAL | ACLs, forgery, company roles, endpoint scope and race tests; comprehensive plan incomplete. | release/installation/fresh.log |
| P03-AC-064 | Company isolation | PASSED | Baseline isolation plus cross-company mapping and scoped RPC results verified. | release/installation/fresh.log |
| P03-AC-065 | No real-order execution | PASSED | Read-only operation allowlist, no mutable real broker or accounting paths. | release/security/source-scan.log; unit/python.log |
| P03-AC-066 | No actionable real-market leakage | PASSED | Synthetic experiments and historical NO TRADE only. | release/browser/edge.log; unit/python.log |
| P03-AC-067 | Fresh installation | PASSED | Actual Odoo 20 clean install passed 10 tests. | release/installation/fresh.log |
| P03-AC-068 | Populated P02 upgrade | PASSED | Independent populated clone preserved records, snapshot hashes and 180 XML IDs. | migration/upgrade/retention.log |
| P03-AC-069 | Complete owner documentation | PASSED | Owner instructions cover delivered offline workflows and provider prerequisites. | docs/OWNER_QUICK_START.md |
| P03-AC-070 | Evidence-backed development handoff | PASSED | Report, criteria, evidence, sanitized source and archive checksum verified. | manifest.sha256; P03_REVIEW_HANDOFF.zip.sha256 |

| ID | Criterion | Status | Scope and evidence (under docs/evidence/p04 unless specified) |
| --- | --- | --- | --- |
| P04-AC-001 | P03 source and evidence preserved | PASSED | P03 checkpoint and historical evidence; baseline/hash.log; baseline/source.sha256 |
| P04-AC-002 | Complete previous regression executed | PASSED | Preserved P03 Python, ORM, contention and Edge re-executed; baseline/odoo; baseline/unit.log |
| P04-AC-003 | Independent review findings investigated | PASSED | Twelve findings assessed with causes and tests; docs/P04_REVIEW_ISSUES.md |
| P04-AC-004 | Confirmed critical defects repaired | PARTIAL | Two reviewed risk defects repaired; provider and orchestration limits remain. |
| P04-AC-005 | Traceability reconciled | PARTIAL | Affected rows reconciled; complete row-by-row revalidation remains open. |
| P04-AC-006 | Secure provider session management | PARTIAL | Process-local five-minute token retention and reauthentication. Real account session unverified. |
| P04-AC-007 | Operational historical synchronization | PARTIAL | Complete one-session fixture workflow and explicitly opt-in real call path. Authorized smoke required. |
| P04-AC-008 | Fixture-backed provider-to-ORM pipeline | PASSED | Adapter, mapping, session validation, storage, idempotency and audit; release/installation/fresh.log |
| P04-AC-009 | Authorized historical integration verified | BLOCKED | Owner entitlement, verified source semantics, approved data or cost evidence required. |
| P04-AC-010 | Instrument master synchronization | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-011 | Shared provider quota enforcement | PASSED | Three operation keys; concurrent local reservation and immediate retry denied; quota.log |
| P04-AC-012 | Market timestamp and freshness contract | PARTIAL | Offset-aware quote parsing, stale threshold and distinct receipt. Documented offset-less format remains unknown. |
| P04-AC-013 | Authorized live quote verification | BLOCKED | Owner entitlement, verified source semantics, approved data or cost evidence required. |
| P04-AC-014 | Streaming implementation and fixture recovery | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-015 | Real streaming verification | BLOCKED | Owner entitlement, verified source semantics, approved data or cost evidence required. |
| P04-AC-016 | Unified data eligibility enforcement | PARTIAL | Origin, quarantine, date and grid checks keep broker history descriptive only. No general policy engine. |
| P04-AC-017 | Secure owner setup workflow | PASSED | Administrator wizard and local-only setup guide; docs/OWNER_ACTION_REQUIRED.md |
| P04-AC-018 | Complete indicator reference tests | PARTIAL | Added 19-output constant/zero-volume reference; full independent indicator matrix incomplete. |
| P04-AC-019 | Unified research engine registry | PARTIAL | P03 supplemental registry and legacy indicators coexist. |
| P04-AC-020 | Core OHLCV research algorithms | PARTIAL | Seven partial scoped research engines inherited. |
| P04-AC-021 | Research provenance and causality | PARTIAL | Causal reference and receipt-only availability tested. Vendor publication evidence unavailable. |
| P04-AC-022 | Benchmark alignment and regime classification | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-023 | Corporate action derived-data integrity | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-024 | Historical universe integrity | BLOCKED | Owner entitlement, verified source semantics, approved data or cost evidence required. |
| P04-AC-025 | Verified tariff configuration | BLOCKED | Owner entitlement, verified source semantics, approved data or cost evidence required. |
| P04-AC-026 | Independent cost calculation reconciliation | PARTIAL | Hypothetical fee fixtures only; contract-note reconciliation unavailable. |
| P04-AC-027 | Authorized historical replay eligibility | BLOCKED | Owner entitlement, verified source semantics, approved data or cost evidence required. |
| P04-AC-028 | Complete ST-01 research behavior | PARTIAL | Synthetic multi-2 loss suspension; market validation and complete ST-01 policy coverage pending. |
| P04-AC-029 | Additional distinct strategy candidate | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-030 | Multi-instrument portfolio replay | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-031 | Shared portfolio capital integrity | PARTIAL | Single-instrument sequential synthetic capital plus exact virtual account gate. |
| P04-AC-032 | Sealed temporal partitions | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-033 | Holdout consumption control | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-034 | Walk-forward validation | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-035 | Financial metrics correctness | PARTIAL | Inherited synthetic metrics regression passed. Portfolio and uncertainty statistics pending. |
| P04-AC-036 | Actual historical financial experiment | BLOCKED | Owner entitlement, verified source semantics, approved data or cost evidence required. |
| P04-AC-037 | Out-of-sample financial evidence | BLOCKED | Owner entitlement, verified source semantics, approved data or cost evidence required. |
| P04-AC-038 | Statistical uncertainty and sensitivity | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-039 | Fee-aware position sizing | PASSED | Prior sizing regression run with P04 suite; unit/python.log |
| P04-AC-040 | Daily portfolio risk enforcement | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-041 | Consecutive-loss suspension | PASSED | Third losing fixture session suspended; unit/python.log |
| P04-AC-042 | Capital-state mismatch protection | PASSED | Frozen cash mismatch rejected under row lock; release/installation/fresh.log |
| P04-AC-043 | Atomic reservation and exposure limits | PARTIAL | Atomic historical account lock and reservation. Portfolio aggregate exposure absent. |
| P04-AC-044 | Complete G01–G14 decision pipeline | PARTIAL | Existing NO TRADE and synthetic gate; complete G01–G14 not implemented. |
| P04-AC-045 | Hard veto protection | PASSED | Independent sizing veto and two-loss hard guard in synthetic scope; unit/python.log |
| P04-AC-046 | Explainable research ranking | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-047 | Persistent paper execution lifecycle | PARTIAL | Historical reserve/simulate/close journal only. |
| P04-AC-048 | Partial fill and close integrity | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-049 | Paper ledger reconciliation | PASSED | Whole-paise independent reconciliation and concurrent journal; replay.json; release/security/contention.log |
| P04-AC-050 | Paper restart recovery | PARTIAL | Idempotent retry with independent contention; full service restart unverified. |
| P04-AC-051 | Historical/prospective isolation | PASSED | Synthetic-only ledger and provider-origin restriction; release/installation/fresh.log |
| P04-AC-052 | Independent worker contention | PASSED | Independent candle, mapping, account and request quota contention; release/security/contention.log; quota.log |
| P04-AC-053 | Job lease and retry recovery | PARTIAL | Inherited transactional one-row claim. Durable lease and retries pending. |
| P04-AC-054 | Exchange-aware daily research | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-055 | Functional stock scanner | PASSED | Company historical scanner and pagination enabled. No ranking; release/browser/edge.log |
| P04-AC-056 | Advanced stock terminal | PARTIAL | Existing chart and findings, new scanner and sync links; full advanced stock terminal pending. |
| P04-AC-057 | Research opportunities dashboard | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-058 | Paper portfolio dashboard | PARTIAL | Virtual-account overview counts and historical journal only. |
| P04-AC-059 | Strategy intelligence dashboard | PARTIAL | Synthetic experiment results and native drill-down. |
| P04-AC-060 | Risk control dashboard | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-061 | Provider health dashboard | PARTIAL | Native sync history and successful-sync count; dedicated health, latest quote and streaming pending. |
| P04-AC-062 | Daily research report | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-063 | KPI reconciliation | PASSED | Underlying historical chart, prior counters and new sync card; release/browser/edge.log |
| P04-AC-064 | Real desktop and mobile browser tests | PASSED | Nine checks including mobile; release/browser/edge.log |
| P04-AC-065 | Light and dark theme verification | NOT_RUN | No verified P04 execution for this criterion. |
| P04-AC-066 | End-to-end performance measurements | PASSED | 50 instruments and 3,750 synthetic bars; migration/performance/orm.json |
| P04-AC-067 | Resource-pressure protection | PARTIAL | Session/response boundaries imposed; resource-pressure testing remains open. |
| P04-AC-068 | Full targeted security regression | PARTIAL | Targeted ACL, adapter endpoint and scanner protections tested. Full security program incomplete. |
| P04-AC-069 | Company isolation | PASSED | Original and scoped new ACL checks; release/installation/fresh.log |
| P04-AC-070 | No real-order execution | PASSED | Existing fixed endpoint and static scan; unit/python.log; source-scan.log |
| P04-AC-071 | No actionable real-market leakage | PASSED | Historical-only scanner and provider data barred from replay; release/browser/edge.log |
| P04-AC-072 | Fresh installation | PASSED | 11 Odoo test cases; release/installation/fresh.log |
| P04-AC-073 | Populated P03 upgrade | PASSED | Populated clone retained 494 XML IDs and original record hashes; migration/upgrade/retention.log |
| P04-AC-074 | Owner setup documentation | PASSED | Read-only local setup, entitlement and sanitized proof; docs/OWNER_ACTION_REQUIRED.md |
| P04-AC-075 | Complete evidence-backed handoff | PASSED | Report, source, evidence, ZIP and checksum; manifest.sha256 |

## 14 — Financial research results

The P03 replay was reproduced and the revised service was verified on synthetic candles, with hypothetical fees and closed virtual entries. An additional three-session fixture showed that the third session is suspended after two losses. No authorized point-in-time market experiment, holdout, calibrated win rate, verified fees or prospective paper P&L were measured. [Replay](docs/evidence/p04/replay.json)

## 15 — Performance results

50 synthetic instruments, 3,750 bars, 361 SQL statements and 4.110 s wall time. Ingestion 1.915 s, research 1.121 s, peak sampled RSS 141.0 MiB. This is actual synthetic Odoo ingest and research throughput on the test workstation. The result does not measure a live market feed, a portfolio or production dashboard latency. [Raw results](docs/evidence/p04/migration/performance/orm.json)

## 16 — Security verification

P04 preserves fixed broker HTTP operations, uses administrator-only synchronization, and gives viewers read-only company-scoped history. The Odoo regression rejected a forged provider dataset and unauthorized wizard creation. Position capital is checked under its existing account row lock before ledger mutation. Static source and package secret patterns were checked. No real-order or live automatic recommendation route was added.

## 17 — Errors and bug fixes

An early install failed because Odoo reserves a different set of selection deletion policies. Adding the origin to the declared base field repaired registry initialization. Existing SQL duplicate and exclusion errors in passing logs were expected rollback assertions. The issue register describes each review finding, reproduction and scope. [Issue register](docs/P04_REVIEW_ISSUES.md)

## 18 — Incomplete features

Authorized real history, live quote, instrument-master synchronization, streaming, verified provider limits, full data eligibility and health, as-of market data and applicable verified tariffs remain open. Multi-instrument replay, checkpointing, sealed holdout, walk-forward, aggregate portfolio risk, durable job leases, complete decision gates, broader research and dashboard validation and prospective paper trading also remain open.

## 19 — Development completion metrics

P04 passed **24/75** criteria. 8 blocked, 25 partial and 18 not run. Original comparable and corrected coverage were not recomputed as a release-wide measure because the full inherited matrix was not independently adjudicated. The preserved P03 reference is 73/1,236 comparable, 57/1,211 corrected, 14/50 original, 30/40 P02 and 29/70 P03. Seven research engines remain partial and zero strategies are financially validated. Percentages from previous milestones are historical snapshots, with denominators as disclosed in those reports.

## 20 — Next development recommendations

Confirm authorization and timestamp semantics and execute one real closed-session read-only smoke. Add verified publication lineage and applicable historical tariffs before sealed as-of financial experiments. Keep prospective execution disabled until broader risk, lifecycle and feed requirements are tested.

## 21 — Owner setup instructions

Install or upgrade P04 through normal Odoo administration after backing up the target database. Assign a Trading System Administrator for mappings, calendar revisions and historical synchronization. Use fixture mode without credentials, or follow the protected host setup and provider authorization steps. [Owner actions](docs/OWNER_ACTION_REQUIRED.md)

## 22 — Final readiness decision

**PAPER TRADING TEST READY for bounded historical synthetic replay only.** P04 also establishes fixture-proven provider-to-ORM ingestion and a functioning historical scanner. Real access, financial validation and prospective paper readiness remain unestablished. Real order execution and actionable real-market recommendations are prohibited.
