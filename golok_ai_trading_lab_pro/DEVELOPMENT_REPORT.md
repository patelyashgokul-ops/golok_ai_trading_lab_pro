# Golok AI Trading Lab Pro — P03 development report

## 01 — Executive summary

**PAPER TRADING TEST READY for bounded historical synthetic replay.** P03 integrates effective-dated instrument records, corporate-action provenance, split calendars, supplemental OHLCV findings, Odoo synthetic experiments, a virtual replay journal, provider diagnostics and a historical research queue. The original read-only market boundary and NO TRADE decision remain in force.

The populated P02 upgrade retained 180 XML IDs and original instrument, dataset, candle and snapshot record hashes. Real broker access, verified financial validation and prospective paper execution remain open. No real-money functionality is enabled.

## 02 — Actual environment

Rechecked 24 November 2026 in Asia/Kolkata. Windows NT 10.0.26300 on an Intel i5-10210U with four physical/eight logical cores, approximately 16 GB RAM, Intel UHD graphics, Python 3.14.6, PostgreSQL 18.4 and Odoo 20 Community. Real UI checks used Edge through Playwright. PostgreSQL's `btree_gist` is required for mapping exclusion constraints. Runtime still uses native Odoo, PostgreSQL and the standard library. Tests ran on disposable localhost databases. No Git repository was present in the addon or containing add-on directory.

## 03 — Architecture implemented

P03 retains all original models and XML IDs. Immutable company-scoped instrument mappings sit beside the original instrument ID. Optional mapping links validate dates and tick sizes during temporal CSV imports. Calendar windows can represent interruptions, and the corporate action record stores publication and revision independently of raw candles.

Odoo snapshots retain the original calculation and input hashes. Supplemental research calculates from the verified original window. Synthetic experiments reuse fixed ST-01, Decimal cost and risk code, and persist single-instrument multi-session outcomes. The historical journal records virtual cash and quantities under account-row locking. The queue claims one historical research request per invocation. Server-side SmartAPI diagnostics require opt-in credentials and do not persist a token. [Architecture](docs/ARCHITECTURE.md)

## 04 — Files created and modified

| Requirements | Path | Before → P03 | Remaining boundary | Verification |
|---|---|---|---|---|
| P03-AC-006–010 | `models/reference.py`, `services/calendar.py`, `views/p03.xml` | Memory-only mapping → persistent exclusion-protected reference and split sessions | Master sync, adjusted curves and point-in-time universe | Odoo mapping test, independent exclusion race, calendar unit |
| P03-AC-011–019 | `models/provider.py` | REST outside Odoo → admin diagnostics, offline gate and database reservation | Historical/quote ingestion, shared market quota and streaming | Offline Odoo diagnostics and three REST fixtures |
| P03-AC-021–023 | `services/research_v3.py`, `models/findings.py` | Three legacy outputs → four additional supplemental findings | Broader research framework and market regime validation | Python warm-up/precedence, ORM digest and Edge drill-down |
| P03-AC-025–039 | `models/experiments.py`, `wizard/experiments.py`, `services/experiments.py` | Single service fixture → persisted Odoo fee-aware multi-session replay | Verified tariffs, multi-instrument portfolio and holdout | Python unresolved data, two-session ORM replay, native browser navigation |
| P03-AC-041–048 | `models/paper.py`, `services/paper.py`, `wizard/paper.py` | No ledger → exact paise, atomic reservations and completed historical fills | Live/prospective monitoring and persistent open positions | Independent reconstruction, insufficient cash, idempotent ORM and real PostgreSQL contention |
| P03-AC-049–051 | `models/jobs.py`, `views/p03.xml` | Manual synchronous only → persistent bounded research worker | Daily orchestration and independent worker-restart scenarios | Requester permissions, idempotency, cancellation, completion |
| P03-AC-052–061 | `static/src/overview.js`, `scripts/verify_browser.py` | P02 counts and OHLC → supplement and experiment/virtual journal entry points | Full dedicated terminal, scanner and multi-panel portfolio | Eight Edge checks, actual ORM throughput |
| P03-AC-067–070 | `scripts/verify_odoo.ps1`, `scripts/verify_p01_upgrade.ps1`, documentation | P02 established → reproducible P03 fresh/upgrade, populated clone and reviewer archive | Release-wide acceptance incomplete | Runtime logs, checksums, clone fingerprints |

## 05 — Requirement traceability matrix

The reconciled matrix preserves the original requirements and all 796 P02 detail IDs. It corrects PostgreSQL from optional to mandatory, updates implemented indicator/reference/replay/virtual scopes, and records original, P02 and P03 outcomes with their evidence. All 70 P03 criteria are reproduced in Section 13. The full matrix and the wording of all three prompts are packaged alongside this report. [Traceability matrix](docs/REQUIREMENTS_TRACEABILITY.md) · [Governing requirements](docs/MASTER_REQUIREMENTS.md)

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

## 07 — Strategy status

| ID | Strategy | Implementation | Financial validation and eligibility |
| --- | --- | --- | --- |
| ST-01 | Opening Range Breakout | multi-1; executed in Odoo on synthetic data | Not validated; real-market ineligible |
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

Three inherited deterministic provider fixture tests passed. Runtime transport is allowlisted HTTPS and P03 has local authorization and offline diagnostics. No authorized authentication, historical market retrieval, live quote or streaming request ran during this milestone. A diagnostics success would not establish observation freshness. Operational ingestion and streaming remain unimplemented. Authoritative account entitlement, egress, current limits and charges require owner/provider confirmation. [Provider operations](docs/PROVIDER_OPERATIONS.md) · [Official SmartAPI SDK](https://github.com/angel-one/smartapi-python)

## 09 — Dashboard development status

| Area | Delivered scope | Open scope |
|---|---|---|
| A Market Command Center | Company counts, historical snapshot, NO TRADE and last ingestion | Live market, market depth and automatic readiness |
| B Stock Scanner | Searchable dated mapping directory and native research lists | Multi-instrument candidate scanner and ranking |
| C Research Opportunities | Historical observations remain NO TRADE | Full gates, eligibility and scoring |
| D Stock Research Terminal | Actual OHLC/volume and supplemental research drill-down | Indicator overlays and broader controls |
| E Paper Portfolio | Virtual accounts and replay cash journal | Live marks, open positions and prospective evaluation |
| F Strategy Intelligence | Synthetic experiment records and drill-down | Segmented holdout, richer diagnostics and strategy metrics |
| G Risk Control | Cost and risk data captured in synthetic run | Dedicated risk dashboard or aggregate portfolio controls |
| H Provider and System Health | Offline SmartAPI detail dialog and historical queue | Live provider and resource health |
| I Daily Research Report | Historical snapshot and list paths | Automated daily report |
| Readiness Center | Static research-only state and provenance | Dedicated readiness gates and acceptance dashboard |

[Desktop screenshot](docs/evidence/p03/release/screenshots/overview-desktop.png) · [Mobile screenshot](docs/evidence/p03/release/screenshots/overview-mobile.png) · [Edge outputs](docs/evidence/p03/release/browser/edge.log)

## 10 — Complete test inventory

P03 final package counts 97 passing executions (40 archive-baseline, 57 final), zero final failures, 5 blocked cases and 10 planned groups not run. Earlier failed retries are logged separately. Each line below has a unique marker. The archive executes P02 including P01 regression cases, and the tested P03 source executes the final expanded suite. No grouped P02 footnote was counted as a case.

| Execution ID | Named case | Status | Evidence or blocker |
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
| B-F-01 | test_database_duplicate_constraint | PASSED | baseline/p02-retest/installation/fresh.log |
| B-F-02 | test_gap_disables_findings | PASSED | baseline/p02-retest/installation/fresh.log |
| B-F-03 | test_import_retry_and_atomic_conflict | PASSED | baseline/p02-retest/installation/fresh.log |
| B-F-04 | test_permissions_and_company_scope | PASSED | baseline/p02-retest/installation/fresh.log |
| B-F-05 | test_point_in_time_calendar_quarantine_and_chart | PASSED | baseline/p02-retest/installation/fresh.log |
| B-F-06 | test_research_cutoff_evidence_and_no_trade | PASSED | baseline/p02-retest/installation/fresh.log |
| B-UO-01 | test_database_duplicate_constraint | PASSED | baseline/p02-retest/installation/upgrade.log |
| B-UO-02 | test_gap_disables_findings | PASSED | baseline/p02-retest/installation/upgrade.log |
| B-UO-03 | test_import_retry_and_atomic_conflict | PASSED | baseline/p02-retest/installation/upgrade.log |
| B-UO-04 | test_permissions_and_company_scope | PASSED | baseline/p02-retest/installation/upgrade.log |
| B-UO-05 | test_point_in_time_calendar_quarantine_and_chart | PASSED | baseline/p02-retest/installation/upgrade.log |
| B-UO-06 | test_research_cutoff_evidence_and_no_trade | PASSED | baseline/p02-retest/installation/upgrade.log |
| B-UI-01 | UI-01 authenticated OWL dashboard and empty state | PASSED | baseline/p02-retest/browser/edge.log |
| B-UI-02 | UI-02 CSV selected and imported through the Odoo wizard | PASSED | baseline/p02-retest/browser/edge.log |
| B-UI-03 | UI-06 database-backed OHLC and volume matched the uploaded fixture | PASSED | baseline/p02-retest/browser/edge.log |
| B-UI-04 | UI-03 historical research, accurate KPIs, refresh and snapshot drill-down | PASSED | baseline/p02-retest/browser/edge.log |
| B-UI-05 | UI-04 mobile viewport without horizontal overflow and no uncaught page errors | PASSED | baseline/p02-retest/browser/edge.log |
| B-UI-06 | UI-05 refresh gracefully recovered from a failed dashboard RPC | PASSED | baseline/p02-retest/browser/edge.log |
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
| P-F-01 | test_database_duplicate_constraint | PASSED | release/installation/fresh.log |
| P-F-02 | test_gap_disables_findings | PASSED | release/installation/fresh.log |
| P-F-03 | test_import_retry_and_atomic_conflict | PASSED | release/installation/fresh.log |
| P-F-04 | test_p03_job_worker_and_immutable_corporate_source | PASSED | release/installation/fresh.log |
| P-F-05 | test_p03_mapping_date_scope_and_database_exclusions | PASSED | release/installation/fresh.log |
| P-F-06 | test_p03_supplemental_findings_and_offline_provider_setup | PASSED | release/installation/fresh.log |
| P-F-07 | test_p03_synthetic_workflow_and_reproducible_immutable_results | PASSED | release/installation/fresh.log |
| P-F-08 | test_permissions_and_company_scope | PASSED | release/installation/fresh.log |
| P-F-09 | test_point_in_time_calendar_quarantine_and_chart | PASSED | release/installation/fresh.log |
| P-F-10 | test_research_cutoff_evidence_and_no_trade | PASSED | release/installation/fresh.log |
| P-UO-01 | test_database_duplicate_constraint | PASSED | release/installation/upgrade.log |
| P-UO-02 | test_gap_disables_findings | PASSED | release/installation/upgrade.log |
| P-UO-03 | test_import_retry_and_atomic_conflict | PASSED | release/installation/upgrade.log |
| P-UO-04 | test_p03_job_worker_and_immutable_corporate_source | PASSED | release/installation/upgrade.log |
| P-UO-05 | test_p03_mapping_date_scope_and_database_exclusions | PASSED | release/installation/upgrade.log |
| P-UO-06 | test_p03_supplemental_findings_and_offline_provider_setup | PASSED | release/installation/upgrade.log |
| P-UO-07 | test_p03_synthetic_workflow_and_reproducible_immutable_results | PASSED | release/installation/upgrade.log |
| P-UO-08 | test_permissions_and_company_scope | PASSED | release/installation/upgrade.log |
| P-UO-09 | test_point_in_time_calendar_quarantine_and_chart | PASSED | release/installation/upgrade.log |
| P-UO-10 | test_research_cutoff_evidence_and_no_trade | PASSED | release/installation/upgrade.log |
| P-UI-01 | UI-01 authenticated OWL dashboard and empty state | PASSED | release/browser/edge.log |
| P-UI-02 | UI-02 CSV selected and imported through the Odoo wizard | PASSED | release/browser/edge.log |
| P-UI-03 | UI-06 database-backed OHLC and volume matched the uploaded fixture | PASSED | release/browser/edge.log |
| P-UI-04 | UI-03 historical research, accurate KPIs, refresh and snapshot drill-down | PASSED | release/browser/edge.log |
| P-UI-05 | UI-07 supplemental evidence generated and opened from the research snapshot | PASSED | release/browser/edge.log |
| P-UI-06 | UI-04 mobile viewport without horizontal overflow and no uncaught page errors | PASSED | release/browser/edge.log |
| P-UI-07 | UI-05 refresh gracefully recovered from a failed dashboard RPC | PASSED | release/browser/edge.log |
| P-UI-08 | UI-08 company experiment and virtual-account cards opened their native lists | PASSED | release/browser/edge.log |
| B-C-01 | identical overlap | PASSED | baseline/p02-retest/security/contention.log |
| B-C-02 | conflicting overlap | PASSED | baseline/p02-retest/security/contention.log |
| P-C-01 | identical overlap | PASSED | release/security/contention.log |
| P-C-02 | conflicting overlap | PASSED | release/security/contention.log |
| P-C-03 | instrument mapping overlap | PASSED | release/security/contention.log |
| P-C-04 | virtual posting overlap | PASSED | release/security/contention.log |
| B-S01 | Archived runtime source audit | PASSED | baseline/source-scan.log |
| B-S02 | Archived synthetic replay reproduction | PASSED | baseline/synthetic.json |
| P-S01 | P03 runtime source audit | PASSED | release/security/source-scan.log |
| P-S02 | Two-session fixture and independent ledger reconciliation | PASSED | backtesting/synthetic-replay-ledger.json |
| P-M01 | Populated P02 clone migration and retention fingerprint | PASSED | migration/upgrade/retention.log |
| P-M02 | 50-instrument end-to-end benchmark | PASSED | migration/performance/orm.json |
| EXT01 | Authorized provider historical request | BLOCKED | Owner entitlement, credentials and static egress |
| EXT02 | Live quote | BLOCKED | No authorized account session |
| EXT03 | WebSocket | BLOCKED | No authorized live entitlement; implementation pending |
| FIN01 | Verified fee reconciliation | BLOCKED | No verified tariff history or authorized contract note |
| FIN02 | Actual financial validation | BLOCKED | No licensed as-of data, sealed partitions or verified tariffs |
| PLAN-01 | Adjustments/universe | NOT_RUN | P03 governing test priorities |
| PLAN-02 | Full indicator boundaries | NOT_RUN | P03 governing test priorities |
| PLAN-03 | Portfolio and market regime | NOT_RUN | P03 governing test priorities |
| PLAN-04 | Multi-instrument replay | NOT_RUN | P03 governing test priorities |
| PLAN-05 | Holdout and walk-forward | NOT_RUN | P03 governing test priorities |
| PLAN-06 | Prospective lifecycle/restart | NOT_RUN | P03 governing test priorities |
| PLAN-07 | Scheduler worker overlap | NOT_RUN | P03 governing test priorities |
| PLAN-08 | Dashboard themes/scanner | NOT_RUN | P03 governing test priorities |
| PLAN-09 | Larger capacity and resource-pressure | NOT_RUN | P03 governing test priorities |
| PLAN-10 | Complete security program | NOT_RUN | P03 governing test priorities |

## 11 — Actual test execution evidence

The separate command inventory lists executable commands, stage times where observed, exit codes, and evidence. The final verification installed and upgraded the addon on Odoo 20, ran contention on independent connections and exercised Edge. The previous P02 clone retained 180 XML IDs, 24 candles, two datasets, two instruments and one immutable snapshot. The original database remained intact. [Commands and timings](docs/evidence/p03/COMMANDS.md) · [Migration](docs/evidence/p03/migration/upgrade/retention.log) · [Evidence hashes](docs/evidence/p03/manifest.sha256)

## 12 — Business invariant verification

| ID | Invariant | Status | Path | Test | Evidence | Remaining scope |
| --- | --- | --- | --- | --- | --- | --- |
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
| INV-12 | No unauthorized broker credential exposure | PARTIAL | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | No credential field or adapter exists. Add real sensitive-field and logging tests when integration is implemented. |
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
| INV-23 | No unbounded background processing | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | U04, P01 | `docs/evidence/performance/services.csv` | Current paths are bounded and manual. Add bounded scheduling when implemented. |
| INV-24 | No paper profit represented as real profit | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-25 | No test marked PASSED without execution evidence | COMPLETE | `DEVELOPMENT_REPORT.md` | D01 | Sections 10–15 and 22 | No financial performance or production readiness claimed. |
| INV-26 | No unsupported market data entitlement bypass | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-27 | No missing required data treated as positive evidence | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-28 | No historical signal deletion to hide losses | PARTIAL | `services/research.py`, `models/lab.py` | O05, O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Snapshot input hashes and role-level immutability exist. Add experiment parameters, amendments and prospective outcomes. |
| INV-29 | No dashboard KPI without a defined data source | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-30 | No production-readiness claim with unresolved critical blockers | COMPLETE | `DEVELOPMENT_REPORT.md` | D01 | Sections 10–15 and 22 | No financial performance or production readiness claimed. |

## 13 — Acceptance criteria verification

The tables below distinguish original requirements, P02 criteria after scoped P03 re-verification and new P03 acceptance. A pass describes the implemented and tested scope, not a claim of validated broker or financial behavior.

| ID | Requirement | Status | Path | Test | Evidence | Remaining scope |
| --- | --- | --- | --- | --- | --- | --- |
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
| AC-016 | Applicable research capabilities functional | PARTIAL | `services/research.py`, `models/lab.py` | U06–U08, O05–O06 | `docs/evidence/tests/unit.log` | Three descriptive findings exist. Complete the remaining indicator set, evidence contract and engine methods. |
| AC-017 | Versioned strategy framework | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | ST-01 version and code hashes; general strategy lifecycle pending. |
| AC-018 | Market regime detection | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-019 | Explainable master decision engine | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | NO TRADE with temporal and quarantine gates. Master gates pending. |
| AC-020 | Transparent quality scoring | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-021 | Risk veto enforcement | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-022 | Transaction cost calculation | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Effective-dated cost engine works with documented hypothetical tariffs. |
| AC-023 | Expected net return calculation | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Synthetic net results v1. Validated evidence and calibration remain. |
| AC-024 | Position sizing validation | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Fee-aware sizing and stop risk verified for the synthetic slice. |
| AC-025 | Signal freshness and expiry | PARTIAL | `services/research.py`, `models/lab.py` | O05–O06 | `docs/evidence/installation/{fresh,upgrade}.log` | NO TRADE blocks actionable historical signals. Implement live freshness or expiry gates before enabling actionable signals. |
| AC-026 | Historical backtesting | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Complete synthetic session replay. Authorized market and multi-session datasets pending. |
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
| AC-041 | Real browser UI verified | PARTIAL | `scripts/verify_browser.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Six focused real-browser checks. Full chart/filters/themes coverage incomplete. |
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
| --- | --- | --- | --- | --- |
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

| Criterion | Requirement | Software verification | Scope and remaining work | Evidence paths |
| --- | --- | --- | --- | --- |
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

## 14 — Financial research results

The redistributable fixture contains two synthetic regular sessions with one simulated trade per session and hypothetical fees. Fixture opening 5,000,000 paise, closing 4,987,596 paise, 6 journal events, no remaining reserved cash or quantity. These monetary figures describe test fixtures. Actual historical experiments, out-of-sample evaluations, walk-forward results, and prospective paper results were unavailable. No real strategy was financially validated. [Replay and independent ledger calculation](docs/evidence/p03/backtesting/synthetic-replay-ledger.json)

## 15 — Performance results

50 synthetic instruments, 3,750 bars and 361 SQL statements. Wall 4.977 s, import 2.335 s, research 1.464 s, company count 2.73 ms. CPU 3.438 s, peak sampled Odoo RSS 138.9 MiB, system RAM available 3.53 GiB at start. This is actual synthetic local ingestion and research using Odoo and PostgreSQL. Larger datasets, resource pressure, broker throughput and browser latency are not measured. [Raw ORM results](docs/evidence/p03/migration/performance/orm.json)

## 16 — Security verification

The role-path regression covers legacy company rules, administrator mapping and provider wizard restrictions, forged experiment/account fields, immutable snapshots and ledger access. P03 confirmed the REST operation allowlist with fixtures and inspected 33 runtime files. PostgreSQL tests exercised actual overlapping mapping and virtual replay writes. Provider secrets are process-local and the final evidence logs received a credential-pattern check. Full cross-company test permutations, transport authorization, and worker-restart review remain incomplete. [Security model](docs/SECURITY_MODEL.md)

## 17 — Errors and bug fixes

The interrupted P03 state had a manifest entry for a missing native view. The view was added and verified in fresh and populated installs. An intermediate regression found that repeated use of the underscore name in diagnostics shadowed Odoo translation; the final ORM case passes with configuration and authentication actions in offline mode. The release regression also rejected forged diagnostic states and confirmed four implementation hashes in the frozen experiment. Duplicate and exclusion errors in final logs are expected rollback assertions. No final cases failed. [Intermediate verification](docs/evidence/p03/verification/installation/fresh.log)

## 18 — Incomplete features

Unfinished or blocked work includes authorized provider-to-ORM data and streaming, verified tariff and universe history, corporate adjustment curves, broader quantitative and regime coverage, persistent strategy approval, multi-instrument simulation, sealed holdout and walk-forward, full decision gates, prospective accounting and feed-dependent monitoring, daily scheduling, and the remaining dashboard scope. The P03 criteria and traceability rows preserve these requirements and their dependencies.

## 19 — Development completion metrics

Original coverage using the comparable requirement count is 73/1,236 (P01/P02 archived 72/1,236). Corrected original coverage is 57/1211; PostgreSQL moves from optional into mandatory, so denominator increases by one from P02's 1,210. Original acceptance 14/50. P02 acceptance 30/40 (archived 26/40). P03 acceptance 29/70. Among 46 P03 product capability criteria (excluding evidence, migration, external verification and validation provenance), 14 passed. The remaining P03 acceptance outcomes include 6 blocked, 11 not run and 24 partial. Research scope is seven of 25 engine identifiers with some ORM implementation. One of 20 strategies is implemented in a synthetic scope; zero are financially validated. External provider runtime verification is blocked. The historical ledger and bounded requester-run queue are verified; prospective ledger and full scheduler are beyond the verified slice.

## 20 — Next development recommendations

1. Connect authenticated read-only ingestion to `models/reference.py` and the existing temporal import after provider terms, timestamp semantics and verified entitlement are available.
2. Add corporate-action-adjusted derived data and effective historical universe coverage while retaining independently auditable raw bars.
3. Add immutable partition lineage, one-time holdout sealing, walk-forward and reconciled fee data around `models/experiments.py` and `services/experiments.py`.
4. Add portfolio risk, prospective lifecycle and lease/restart tests before activating anything beyond the historical journal and queue.

## 21 — Owner setup instructions

Install or upgrade only after backup and normal local change review. PostgreSQL must allow the trusted `btree_gist` extension installation. Set Trading Lab roles, enter sourced references, register a dataset and run research. Use a labeled fixture for the Odoo experiment and Risk Manager virtual journal. The scheduled action is disabled by default. Configure provider credentials only on the Odoo host. [Owner quick start](docs/OWNER_QUICK_START.md)

## 22 — Final readiness decision

**PAPER TRADING TEST READY for bounded historical synthetic replay.** Isolated tests prove date-aware reference constraints, version-compatible Odoo research, conservative synthetic replay, historical virtual reconciliation and replay idempotency. They do not establish financial performance, authorized live data access or prospective paper readiness. All real order execution and actionable real-market recommendations remain prohibited.
