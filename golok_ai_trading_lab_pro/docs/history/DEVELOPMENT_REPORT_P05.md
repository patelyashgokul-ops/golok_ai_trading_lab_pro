# Golok AI Trading Lab Pro — P05 development report

## 01 — Executive summary

24 November 2026, Asia/Kolkata. **FOUNDATION VERIFIED for offline historical research and synthetic replay. P05 functional completion remains open.** P05 adds bounded historical sync planning, three synthetic portfolio strategies, shared capital, independent risk limits, chronological fold generation and native Odoo evidence views. Authorized acquisition and statistical validation remain open.

## 02 — Actual environment

Testing used Windows, Odoo 20 Community, PostgreSQL 18.4, Python 3.14.6 for Odoo, Python 3.11.9 for standalone tests and Edge 158.0.4370.33 through Playwright. Odoo execution used disposable local databases. The module directory had no Git metadata. Source and evidence checkpoints use SHA-256.

## 03 — Architecture implemented

The administrator sync plan advances one persistent, bounded task through the existing provider-to-ORM pipeline per request. Attempts and retry time survive requests. Synthetic portfolio replay validates the complete calendar grid for each instrument, processes completed closes before same-timestamp opens, and uses an opening strictly after the candidate's availability. Known losses, aggregate risk and shared cash restrict entries. The immutable company-scoped portfolio record captures input and implementation digests, decisions and ledger.

## 04 — Files created and modified

| Area | P04 | P05 | Source and executed verification | Remaining scope |
| --- | --- | --- | --- | --- |
| Historical acquisition | One closed session | 60 bounded checkpoints | models/sync_plan.py, views/p05.xml, two instruments across two dates in Odoo | Authorized transport, process restart and cross-plan contention |
| Authentication | Five-minute implicit cache | Explicit worker cache with a 30-minute maximum | models/provider.py, services/session_policy.py, Odoo mock and clock tests | Multi-worker routing and real account |
| Eligibility and decisions | Caller-specific checks | Shared eligibility and fourteen synthetic candidate gates | services/eligibility.py, services/decision.py, gate and risk checks | Broader application integration and financial eligibility |
| Research | Four supplemental algorithms | Eight supplemental algorithms | services/research_v3.py, fixtures and native findings workflow | Remaining engines, full indicator references and calibration |
| Strategies | Sequential ST-01 multi-2 | Sequential multi-3 and three portfolio strategies | services/strategies.py, services/experiments.py, signal and replay tests | Full strategy scenarios and approval lifecycle |
| Portfolio | One instrument at a time | Shared capital, aggregate risk and immutable results | services/portfolio.py, models/portfolio.py, fixture, ORM and Edge | Marked risk, exposure groups and richer metrics |
| Temporal evaluation | Fixed snapshots | Frozen chronological dates, embargo and walk-forward folds | services/temporal.py, overlap and holdout exclusion tests | Persistent sealed holdout and fold execution |
| Research terminal | Historical scanner and charts | Native sync plans, portfolio KPI and record drill-down | views/p05.xml, static/src/overview.js, Edge UI-10 and UI-11 | Ranking, full dashboards, mobile forms and themes |

## 05 — Requirement traceability matrix

The matrix retains 4043 prior identifiers and adds 60 P05 acceptance identifiers and 755 P05 detail identifiers. Previously verified scopes remain archived. [Requirements traceability](docs/REQUIREMENTS_TRACEABILITY.md) · [P05 issues](docs/P05_REVIEW_ISSUES.md)

## 06 — Research engine status

Four new persisted supplemental definitions supplement the existing four. Three base engines remain separate. The independent indicator reference matrix remains incomplete.

| ID | Capability | Implementation and regression | Financial validation |
| --- | --- | --- | --- |
| RE-01 | Technical Analysis | Legacy technical indicators | Not established |
| RE-02 | Fundamental Analysis | Pending | Not established |
| RE-03 | Price Action Analysis | Supplemental six-bar structure | Not established |
| RE-04 | Candlestick Pattern Analysis | Supplemental objective candle geometry | Not established |
| RE-05 | Volume Intelligence | Legacy volume and relative-volume findings | Not established |
| RE-06 | Support and Resistance | Supplemental preceding twenty-bar levels | Not established |
| RE-07 | Breakout Detection | Close beyond the prior ten-bar high or low | Not established |
| RE-08 | False Breakout Detection | Re-entry into the pre-breakout range | Not established |
| RE-09 | Market Trend Analysis | Instrument-only regime from causal returns | Not established |
| RE-10 | Sector Performance and Rotation | Pending | Not established |
| RE-11 | Benchmark Index Analysis | Pending | Not established |
| RE-12 | Global Market Context | Pending | Not established |
| RE-13 | Financial News and Event Analysis | Pending | Not established |
| RE-14 | Institutional Activity Proxies | Pending | Not established |
| RE-15 | Historical Pattern Analysis | Pending | Not established |
| RE-16 | Statistical Probability Estimation | Pending | Not established |
| RE-17 | Liquidity Analysis | Median OHLCV turnover proxy and zero-volume count | Not established |
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
| ST-01 | Opening Range Breakout | multi-3 sequential and portfolio-1; archived multi-1/multi-2 results retained | Not validated; real-market ineligible |
| ST-02 | VWAP Pullback | portfolio-1; pullback using prior approximate VWAP | Not validated; real-market ineligible |
| ST-03 | VWAP Reclaim | Not implemented | Not validated; real-market ineligible |
| ST-04 | Trend Following | Not implemented | Not validated; real-market ineligible |
| ST-05 | Momentum Continuation | Not implemented | Not validated; real-market ineligible |
| ST-06 | Volume Confirmed Breakout | Not implemented | Not validated; real-market ineligible |
| ST-07 | Support and Resistance Breakout | Not implemented | Not validated; real-market ineligible |
| ST-08 | Mean Reversion | portfolio-1; downside rejection of preceding six-bar range | Not validated; real-market ineligible |
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

Diagnostics retain explicitly authenticated clients in the current worker. Authentication requires local opt-in and a timestamped fresh TOTP. History requires a separate open-stamped setting and an unexpired worker cache. The local database retains a 60-second quota per operation. No request reached Angel One during P05. Real entitlement, egress, fees, timestamp semantics and API speed require owner confirmation. [Provider documentation](https://smartapi.angelone.in/docs/ResponseStructure) · [Owner setup](docs/OWNER_ACTION_REQUIRED.md)

## 09 — Dashboard development status

Edge verified drill-down into the historical chart, findings, scanner, experiments, virtual accounts and company portfolio list. It opened a persisted portfolio with decisions and frozen inputs after the wizard's server action. The new sync plan was tested through Odoo ORM. Mobile verification covers the overview. Full theme, ranking, dashboard and mobile form coverage remains open. [Edge log](docs/evidence/p05/release/browser/edge.log)

## 10 — Complete test inventory

| Execution ID | Command ID | Expected check | Actual | Exit | Evidence under docs/evidence/p05 | 
| --- | --- | --- | --- | --- | --- | 
| B-U-01 | B01 | test_duplicate_and_reversed_csv | Passed | 0 | baseline/unit.log | 
| B-U-02 | B01 | test_empty_and_size_limits | Passed | 0 | baseline/unit.log | 
| B-U-03 | B01 | test_gap_count_and_date_boundary | Passed | 0 | baseline/unit.log | 
| B-U-04 | B01 | test_invalid_prices_volume_and_timestamps | Passed | 0 | baseline/unit.log | 
| B-U-05 | B01 | test_utc_normalization_and_exact_prices | Passed | 0 | baseline/unit.log | 
| B-U-06 | B01 | test_atr_gaps_wilder_smoothing | Passed | 0 | baseline/unit.log | 
| B-U-07 | B01 | test_reference_values_and_relative_volume_baseline | Passed | 0 | baseline/unit.log | 
| B-U-08 | B01 | test_warmup_and_no_future_access | Passed | 0 | baseline/unit.log | 
| B-U-09 | B01 | test_calendar_and_time_availability | Passed | 0 | baseline/unit.log | 
| B-U-10 | B01 | test_temporal_csv_rejects_early_availability_and_future | Passed | 0 | baseline/unit.log | 
| B-U-11 | B01 | test_reference_values_and_all_prefixes | Passed | 0 | baseline/unit.log | 
| B-U-12 | B01 | test_session_reset_and_opening_range | Passed | 0 | baseline/unit.log | 
| B-U-13 | B01 | test_disabled_transport_and_endpoint_scope | Passed | 0 | baseline/unit.log | 
| B-U-14 | B01 | test_fixture_auth_history_quote_and_rate_limit | Passed | 0 | baseline/unit.log | 
| B-U-15 | B01 | test_timeout_sanitizes_transport_error | Passed | 0 | baseline/unit.log | 
| B-U-16 | B01 | test_token_reuse_and_ineligible_mapping | Passed | 0 | baseline/unit.log | 
| B-U-17 | B01 | test_breakout_reproducibility_and_stop_first | Passed | 0 | baseline/unit.log | 
| B-U-18 | B01 | test_tariffs_effective_date_and_risk | Passed | 0 | baseline/unit.log | 
| B-U-19 | B01 | test_multiple_sessions_stop_at_unknown_calendar_and_reconcile_trades | Passed | 0 | baseline/unit.log | 
| B-U-20 | B01 | test_split_calendar_has_no_cross_segment_bars | Passed | 0 | baseline/unit.log | 
| B-U-21 | B01 | test_supplemental_algorithms_warmup_and_preceding_levels | Passed | 0 | baseline/unit.log | 
| B-U-22 | B01 | test_flat_zero_volume_indicator_reference | Passed | 0 | baseline/unit.log | 
| B-U-23 | B01 | test_provider_normalization_rejects_future_close_and_wrong_stamp | Passed | 0 | baseline/unit.log | 
| B-U-24 | B01 | test_third_losing_session_is_suspended | Passed | 0 | baseline/unit.log | 
| B-U-25 | B01 | test_time_and_receipt_are_distinct | Passed | 0 | baseline/unit.log | 
| B-F-01 | B02 | test_database_duplicate_constraint | Passed | 0 | baseline/odoo/installation/fresh.log | 
| B-F-02 | B02 | test_gap_disables_findings | Passed | 0 | baseline/odoo/installation/fresh.log | 
| B-F-03 | B02 | test_import_retry_and_atomic_conflict | Passed | 0 | baseline/odoo/installation/fresh.log | 
| B-F-04 | B02 | test_p03_job_worker_and_immutable_corporate_source | Passed | 0 | baseline/odoo/installation/fresh.log | 
| B-F-05 | B02 | test_p03_mapping_date_scope_and_database_exclusions | Passed | 0 | baseline/odoo/installation/fresh.log | 
| B-F-06 | B02 | test_p03_supplemental_findings_and_offline_provider_setup | Passed | 0 | baseline/odoo/installation/fresh.log | 
| B-F-07 | B02 | test_p03_synthetic_workflow_and_reproducible_immutable_results | Passed | 0 | baseline/odoo/installation/fresh.log | 
| B-F-08 | B02 | test_p04_fixture_sync_atomic_viewable_and_idempotent | Passed | 0 | baseline/odoo/installation/fresh.log | 
| B-F-09 | B02 | test_permissions_and_company_scope | Passed | 0 | baseline/odoo/installation/fresh.log | 
| B-F-10 | B02 | test_point_in_time_calendar_quarantine_and_chart | Passed | 0 | baseline/odoo/installation/fresh.log | 
| B-F-11 | B02 | test_research_cutoff_evidence_and_no_trade | Passed | 0 | baseline/odoo/installation/fresh.log | 
| B-R-01 | B02 | test_database_duplicate_constraint | Passed | 0 | baseline/odoo/installation/upgrade.log | 
| B-R-02 | B02 | test_gap_disables_findings | Passed | 0 | baseline/odoo/installation/upgrade.log | 
| B-R-03 | B02 | test_import_retry_and_atomic_conflict | Passed | 0 | baseline/odoo/installation/upgrade.log | 
| B-R-04 | B02 | test_p03_job_worker_and_immutable_corporate_source | Passed | 0 | baseline/odoo/installation/upgrade.log | 
| B-R-05 | B02 | test_p03_mapping_date_scope_and_database_exclusions | Passed | 0 | baseline/odoo/installation/upgrade.log | 
| B-R-06 | B02 | test_p03_supplemental_findings_and_offline_provider_setup | Passed | 0 | baseline/odoo/installation/upgrade.log | 
| B-R-07 | B02 | test_p03_synthetic_workflow_and_reproducible_immutable_results | Passed | 0 | baseline/odoo/installation/upgrade.log | 
| B-R-08 | B02 | test_p04_fixture_sync_atomic_viewable_and_idempotent | Passed | 0 | baseline/odoo/installation/upgrade.log | 
| B-R-09 | B02 | test_permissions_and_company_scope | Passed | 0 | baseline/odoo/installation/upgrade.log | 
| B-R-10 | B02 | test_point_in_time_calendar_quarantine_and_chart | Passed | 0 | baseline/odoo/installation/upgrade.log | 
| B-R-11 | B02 | test_research_cutoff_evidence_and_no_trade | Passed | 0 | baseline/odoo/installation/upgrade.log | 
| B-E-01 | B02 | UI-01 authenticated OWL dashboard and empty state | Passed | 0 | baseline/odoo/browser/edge.log | 
| B-E-02 | B02 | UI-02 CSV selected and imported through the Odoo wizard | Passed | 0 | baseline/odoo/browser/edge.log | 
| B-E-03 | B02 | UI-06 database-backed OHLC and volume matched the uploaded fixture | Passed | 0 | baseline/odoo/browser/edge.log | 
| B-E-04 | B02 | UI-03 historical research, accurate KPIs, refresh and snapshot drill-down | Passed | 0 | baseline/odoo/browser/edge.log | 
| B-E-05 | B02 | UI-07 supplemental evidence generated and opened from the research snapshot | Passed | 0 | baseline/odoo/browser/edge.log | 
| B-E-06 | B02 | UI-04 mobile viewport without horizontal overflow and no uncaught page errors | Passed | 0 | baseline/odoo/browser/edge.log | 
| B-E-07 | B02 | UI-05 refresh gracefully recovered from a failed dashboard RPC | Passed | 0 | baseline/odoo/browser/edge.log | 
| B-E-08 | B02 | UI-08 company experiment and virtual-account cards opened their native lists | Passed | 0 | baseline/odoo/browser/edge.log | 
| B-E-09 | B02 | UI-09 historical scanner opens with instrument, company data and NO TRADE | Passed | 0 | baseline/odoo/browser/edge.log | 
| F-U-01 | F01 | test_duplicate_and_reversed_csv | Passed | 0 | unit/python.log | 
| F-U-02 | F01 | test_empty_and_size_limits | Passed | 0 | unit/python.log | 
| F-U-03 | F01 | test_gap_count_and_date_boundary | Passed | 0 | unit/python.log | 
| F-U-04 | F01 | test_invalid_prices_volume_and_timestamps | Passed | 0 | unit/python.log | 
| F-U-05 | F01 | test_utc_normalization_and_exact_prices | Passed | 0 | unit/python.log | 
| F-U-06 | F01 | test_atr_gaps_wilder_smoothing | Passed | 0 | unit/python.log | 
| F-U-07 | F01 | test_reference_values_and_relative_volume_baseline | Passed | 0 | unit/python.log | 
| F-U-08 | F01 | test_warmup_and_no_future_access | Passed | 0 | unit/python.log | 
| F-U-09 | F01 | test_calendar_and_time_availability | Passed | 0 | unit/python.log | 
| F-U-10 | F01 | test_temporal_csv_rejects_early_availability_and_future | Passed | 0 | unit/python.log | 
| F-U-11 | F01 | test_reference_values_and_all_prefixes | Passed | 0 | unit/python.log | 
| F-U-12 | F01 | test_session_reset_and_opening_range | Passed | 0 | unit/python.log | 
| F-U-13 | F01 | test_disabled_transport_and_endpoint_scope | Passed | 0 | unit/python.log | 
| F-U-14 | F01 | test_fixture_auth_history_quote_and_rate_limit | Passed | 0 | unit/python.log | 
| F-U-15 | F01 | test_timeout_sanitizes_transport_error | Passed | 0 | unit/python.log | 
| F-U-16 | F01 | test_token_reuse_and_ineligible_mapping | Passed | 0 | unit/python.log | 
| F-U-17 | F01 | test_breakout_reproducibility_and_stop_first | Passed | 0 | unit/python.log | 
| F-U-18 | F01 | test_tariffs_effective_date_and_risk | Passed | 0 | unit/python.log | 
| F-U-19 | F01 | test_multiple_sessions_stop_at_unknown_calendar_and_reconcile_trades | Passed | 0 | unit/python.log | 
| F-U-20 | F01 | test_split_calendar_has_no_cross_segment_bars | Passed | 0 | unit/python.log | 
| F-U-21 | F01 | test_supplemental_algorithms_warmup_and_preceding_levels | Passed | 0 | unit/python.log | 
| F-U-22 | F01 | test_flat_zero_volume_indicator_reference | Passed | 0 | unit/python.log | 
| F-U-23 | F01 | test_provider_normalization_rejects_future_close_and_wrong_stamp | Passed | 0 | unit/python.log | 
| F-U-24 | F01 | test_third_losing_session_is_suspended | Passed | 0 | unit/python.log | 
| F-U-25 | F01 | test_time_and_receipt_are_distinct | Passed | 0 | unit/python.log | 
| F-U-26 | F01 | test_eligibility_is_fail_closed | Passed | 0 | unit/python.log | 
| F-U-27 | F01 | test_every_gate_vetoes_and_unrecognized_modes_fail | Passed | 0 | unit/python.log | 
| F-U-28 | F01 | test_fixture_reconciles_and_risk_rejects_a_third_instrument | Passed | 0 | unit/python.log | 
| F-U-29 | F01 | test_incomplete_late_and_quarantined_data_reject | Passed | 0 | unit/python.log | 
| F-U-30 | F01 | test_portfolio_suspension_carries_across_completed_sessions | Passed | 0 | unit/python.log | 
| F-U-31 | F01 | test_research_preceding_levels_and_turnover | Passed | 0 | unit/python.log | 
| F-U-32 | F01 | test_session_deadline_and_expired_authorization | Passed | 0 | unit/python.log | 
| F-U-33 | F01 | test_vwap_and_reversion_use_distinct_prior_observations | Passed | 0 | unit/python.log | 
| F-U-34 | F01 | test_walk_forward_excludes_holdout_and_embargo | Passed | 0 | unit/python.log | 
| F-F-01 | F02 | test_database_duplicate_constraint | Passed | 0 | release/installation/fresh.log | 
| F-F-02 | F02 | test_gap_disables_findings | Passed | 0 | release/installation/fresh.log | 
| F-F-03 | F02 | test_import_retry_and_atomic_conflict | Passed | 0 | release/installation/fresh.log | 
| F-F-04 | F02 | test_p03_job_worker_and_immutable_corporate_source | Passed | 0 | release/installation/fresh.log | 
| F-F-05 | F02 | test_p03_mapping_date_scope_and_database_exclusions | Passed | 0 | release/installation/fresh.log | 
| F-F-06 | F02 | test_p03_supplemental_findings_and_offline_provider_setup | Passed | 0 | release/installation/fresh.log | 
| F-F-07 | F02 | test_p03_synthetic_workflow_and_reproducible_immutable_results | Passed | 0 | release/installation/fresh.log | 
| F-F-08 | F02 | test_p04_fixture_sync_atomic_viewable_and_idempotent | Passed | 0 | release/installation/fresh.log | 
| F-F-09 | F02 | test_p05_portfolio_fixture_and_role_boundaries | Passed | 0 | release/installation/fresh.log | 
| F-F-10 | F02 | test_p05_provider_diagnostics_reuse_session_and_do_not_auto_login | Passed | 0 | release/installation/fresh.log | 
| F-F-11 | F02 | test_permissions_and_company_scope | Passed | 0 | release/installation/fresh.log | 
| F-F-12 | F02 | test_point_in_time_calendar_quarantine_and_chart | Passed | 0 | release/installation/fresh.log | 
| F-F-13 | F02 | test_research_cutoff_evidence_and_no_trade | Passed | 0 | release/installation/fresh.log | 
| F-R-01 | F02 | test_database_duplicate_constraint | Passed | 0 | release/installation/upgrade.log | 
| F-R-02 | F02 | test_gap_disables_findings | Passed | 0 | release/installation/upgrade.log | 
| F-R-03 | F02 | test_import_retry_and_atomic_conflict | Passed | 0 | release/installation/upgrade.log | 
| F-R-04 | F02 | test_p03_job_worker_and_immutable_corporate_source | Passed | 0 | release/installation/upgrade.log | 
| F-R-05 | F02 | test_p03_mapping_date_scope_and_database_exclusions | Passed | 0 | release/installation/upgrade.log | 
| F-R-06 | F02 | test_p03_supplemental_findings_and_offline_provider_setup | Passed | 0 | release/installation/upgrade.log | 
| F-R-07 | F02 | test_p03_synthetic_workflow_and_reproducible_immutable_results | Passed | 0 | release/installation/upgrade.log | 
| F-R-08 | F02 | test_p04_fixture_sync_atomic_viewable_and_idempotent | Passed | 0 | release/installation/upgrade.log | 
| F-R-09 | F02 | test_p05_portfolio_fixture_and_role_boundaries | Passed | 0 | release/installation/upgrade.log | 
| F-R-10 | F02 | test_p05_provider_diagnostics_reuse_session_and_do_not_auto_login | Passed | 0 | release/installation/upgrade.log | 
| F-R-11 | F02 | test_permissions_and_company_scope | Passed | 0 | release/installation/upgrade.log | 
| F-R-12 | F02 | test_point_in_time_calendar_quarantine_and_chart | Passed | 0 | release/installation/upgrade.log | 
| F-R-13 | F02 | test_research_cutoff_evidence_and_no_trade | Passed | 0 | release/installation/upgrade.log | 
| F-E-01 | F02 | UI-01 authenticated OWL dashboard and empty state | Passed | 0 | release/browser/edge.log | 
| F-E-02 | F02 | UI-02 CSV selected and imported through the Odoo wizard | Passed | 0 | release/browser/edge.log | 
| F-E-03 | F02 | UI-06 database-backed OHLC and volume matched the uploaded fixture | Passed | 0 | release/browser/edge.log | 
| F-E-04 | F02 | UI-03 historical research, accurate KPIs, refresh and snapshot drill-down | Passed | 0 | release/browser/edge.log | 
| F-E-05 | F02 | UI-07 supplemental evidence generated and opened from the research snapshot | Passed | 0 | release/browser/edge.log | 
| F-E-06 | F02 | UI-04 mobile viewport without horizontal overflow and no uncaught page errors | Passed | 0 | release/browser/edge.log | 
| F-E-07 | F02 | UI-05 refresh gracefully recovered from a failed dashboard RPC | Passed | 0 | release/browser/edge.log | 
| F-E-08 | F02 | UI-08 company experiment and virtual-account cards opened their native lists | Passed | 0 | release/browser/edge.log | 
| F-E-09 | F02 | UI-09 historical scanner opens with instrument, company data and NO TRADE | Passed | 0 | release/browser/edge.log | 
| F-E-10 | F02 | UI-10 portfolio KPI reconciles to the company-scoped native portfolio list | Passed | 0 | release/browser/edge.log | 
| F-E-11 | F02 | UI-11 synthetic replay submitted through Odoo wizard RPC and persisted result, gates and frozen inputs inspected in Edge | Passed | 0 | release/browser/edge.log | 
| F-Q-01 | F04 | QUOTA PASS authenticate: two workers, one committed reservation, immediate retry denied | Passed | 0 | security/quota.log | 
| F-Q-02 | F04 | QUOTA PASS history: two workers, one committed reservation, immediate retry denied | Passed | 0 | security/quota.log | 
| F-Q-03 | F04 | QUOTA PASS quote: two workers, one committed reservation, immediate retry denied | Passed | 0 | security/quota.log | 
| B-C | B02 | Independent baseline database races | Passed | 0 | baseline/odoo/security/contention.log | 
| B-H | B03 | Archived evidence and source hashes | Passed | 0 | baseline/hash.log | 
| B-S | B04 | Archived source inspection | Passed | 0 | baseline/source.log | 
| B-D | B05 | Archived deterministic replay | Passed | 0 | baseline/replay.json | 
| F-C | F02 | Independent database races | Passed | 0 | release/security/contention.log | 
| F-M | F03 | P04 record and XML ID retention | Passed | 0 | upgrade-final/upgrade/retention.log | 
| F-P | F03 | 50-instrument synthetic ORM benchmark | Passed | 0 | upgrade-final/performance/orm.json | 
| F-D | F05 | Matching replays and independent accounting | Passed | 0 | portfolio/fixture.json | 
| F-S | F06 | Release source inspection | Passed | 0 | security/source.log | 
| I-F | I02 | Intermediate diagnostics test | Intermediate failure, corrected | 1 | intermediate/orm-auth-test.log | 
| I-C | I03 | Intermediate shared session cache invalidation test | Intermediate failure, corrected | 1 | intermediate/orm-session-cache.log | 

The command column maps each execution to the exact command and aggregate outcome in the execution index. [Commands](docs/evidence/p05/COMMANDS.md)

## 11 — Actual test execution evidence

Archived P04 reruns passed 25 standalone, 11 fresh and 11 update ORM tests, independent data/account contention and nine browser assertions. Final P05 passed 34 standalone, 13 fresh and 13 update ORM tests, 11 Edge assertions, independent data/account contention and three independent quota races. Populated migration compared database-record hashes. The duplicate and exclusion SQL errors in successful logs are intentional negative tests. [Evidence index](docs/evidence/p05/COMMANDS.md)

## 12 — Business invariant verification

The archived INV-01 through INV-30 dispositions below retain their historical scope. New synthetic eligibility, risk and shared cash checks are mapped in P05 acceptance.

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

P01 through P04 dispositions retain their archived scope and date.

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

### P05 acceptance

| ID | Criterion | Status | Evidence or open scope | 
| --- | --- | --- | --- | 
| P05-AC-001 | P04 source and evidence preserved | PASSED | P04 checkpoint, preserved evidence and verified hashes, baseline/hash.log. | 
| P05-AC-002 | Previous regression executed | PASSED | P04 standalone, ORM, contention and Edge rerun, baseline/. | 
| P05-AC-003 | Twelve review findings investigated | PASSED | All 12 causes and dispositions recorded in docs/P05_REVIEW_ISSUES.md. | 
| P05-AC-004 | Secure provider session lifecycle | PARTIAL | Explicit process-local session with bounded expiry and injected diagnostics verified offline. | 
| P05-AC-005 | Controlled reauthentication | PARTIAL | Fresh timestamped TOTP, no implicit retry and cached diagnostics verified offline. | 
| P05-AC-006 | Configurable verified or qualified quotas | PARTIAL | Fixed local reservation and task retry delay. Verified account quotas and cross-database coordination pending. | 
| P05-AC-007 | Historical synchronization planner | PARTIAL | Native bounded multi-instrument multi-date planner. Operator-triggered processing. | 
| P05-AC-008 | Resumable multi-session ingestion | PARTIAL | Four checkpoints, duplicate replay and cancellation. Forced process restart and real throughput unverified. | 
| P05-AC-009 | Instrument master synchronization | NOT_RUN | Instrument master ingestion and historical universe validation remain open. | 
| P05-AC-010 | Unified source eligibility | PARTIAL | Shared source eligibility for portfolio and supplemental findings. Legacy entry points and live eligibility remain open. | 
| P05-AC-011 | Authorized real historical smoke test | BLOCKED | Owner-approved credentials, entitlement, egress and timestamp semantics unavailable. | 
| P05-AC-012 | Quote freshness contract | PARTIAL | Offset-aware freshness fixture regression. Offset-less provider times remain unknown. | 
| P05-AC-013 | Unified research registry | PARTIAL | Eight supplemental algorithms coexist with three legacy engines. | 
| P05-AC-014 | Indicator reference matrix | PARTIAL | Flat, prefix and selected numerical references rerun. Complete matrix open. | 
| P05-AC-015 | Expanded core research algorithms | PASSED | Four additional persisted research algorithms with causal fixture checks. | 
| P05-AC-016 | Research evidence persistence | PASSED | Versioned findings tied to immutable input digest, release/installation/fresh.log. | 
| P05-AC-017 | Instrument regime classification | PARTIAL | Instrument-only regime with reasons. Full independent regime matrix and benchmark pending. | 
| P05-AC-018 | Persistent multi-strategy framework | PARTIAL | Three implementations with frozen version and hashes. Governance and approval pending. | 
| P05-AC-019 | ST-01 regression and extension | PASSED | ST-01 multi-3 and new portfolio variant plus archived baseline. | 
| P05-AC-020 | ST-02 implementation | PARTIAL | Causal ST-02 exists and signal fixture passed. Full trade-case coverage open. | 
| P05-AC-021 | ST-04 implementation | NOT_RUN | ST-04 remains open. | 
| P05-AC-022 | ST-06 implementation | NOT_RUN | Independent ST-06 remains open. | 
| P05-AC-023 | ST-08 implementation | PARTIAL | Distinct ST-08 signal and fixture. Full trade-case coverage open. | 
| P05-AC-024 | Authorized historical eligibility pathway | PARTIAL | Fail-closed classifications exist. No enabled authorized financial replay. | 
| P05-AC-025 | Versioned transaction costs | PARTIAL | Frozen effective-dated hypothetical tariffs. Real fee evidence and native calculator open. | 
| P05-AC-026 | Independent cost reconciliation | PARTIAL | Independent synthetic cash and fee reconciliation. Actual tariff estimates unverified. | 
| P05-AC-027 | Multi-instrument portfolio replay | PASSED | Multi-instrument replay and shared cash, portfolio/fixture.json and ORM. | 
| P05-AC-028 | Shared virtual capital integrity | PASSED | Per-event cash and fees reconcile with independent arithmetic. | 
| P05-AC-029 | Portfolio risk enforcement | PARTIAL | Aggregate known risk, shared cash, daily and consecutive-loss guards. Sector exposure and marking open. | 
| P05-AC-030 | Daily loss protection | PASSED | A tighter fixture risk budget vetoes the third otherwise eligible entry. | 
| P05-AC-031 | Consecutive-loss and suspension semantics | PASSED | Incomplete date coverage and consecutive-loss pause distinguished in sequential tests. | 
| P05-AC-032 | Independently verified portfolio metrics | PARTIAL | Cash, gross, fees, net and closed-day drawdown. Marked drawdown and uncertainty statistics open. | 
| P05-AC-033 | Immutable chronological partitions | PARTIAL | Frozen date window and embargo. Persistence and signed input freeze pending. | 
| P05-AC-034 | Holdout consumption enforcement | NOT_RUN | Durable single-use holdout consumption remains open. | 
| P05-AC-035 | Walk-forward implementation | PARTIAL | Bounded walk-forward date generation. Automated evaluation per fold open. | 
| P05-AC-036 | Temporal leakage rejection | PARTIAL | Overlap, embargo and late synthetic input rejection tested. Integrated holdout leakage protection open. | 
| P05-AC-037 | Actual historical financial experiment | BLOCKED | Authorized point-in-time inputs, charges and sealed evaluation unavailable. | 
| P05-AC-038 | Complete G01–G14 decision gates | PARTIAL | All fourteen gates veto independently in synthetic portfolio. Complete application integration open. | 
| P05-AC-039 | Hard risk veto | PASSED | G11 rejects an otherwise valid third candidate in deterministic fixture. | 
| P05-AC-040 | Explainable candidate ranking | NOT_RUN | Stable priority exists. Explainable ranking remains open. | 
| P05-AC-041 | Multi-instrument research orchestration | NOT_RUN | Multi-instrument research orchestration remains open. | 
| P05-AC-042 | Worker restart and checkpoint recovery | PARTIAL | Next operator request continues persisted checkpoints. Forced process restart and leases unverified. | 
| P05-AC-043 | Independent worker contention | PARTIAL | Independent import, mapping, paper and quota races. New sync plan contention unverified. | 
| P05-AC-044 | Professional stock scanner | PARTIAL | Existing native scanner browser regression. Ranked scanner pending. | 
| P05-AC-045 | Advanced stock research terminal | PARTIAL | Existing chart and findings browser regression. Advanced terminal pending. | 
| P05-AC-046 | Strategy and risk laboratory | PARTIAL | Native portfolio KPI, records and frozen inputs. Complete strategy-risk workspace pending. | 
| P05-AC-047 | Dashboard numerical reconciliation | PARTIAL | Baseline bars, snapshots and portfolio count reconciled in Edge. All new KPIs pending. | 
| P05-AC-048 | Virtual ledger regression | PASSED | Existing virtual account postings and ledger conservation under independent contention. | 
| P05-AC-049 | Historical/prospective isolation | PARTIAL | Historical posting isolated. Prospective simulation remains gated out. | 
| P05-AC-050 | Real browser workflows | PASSED | Automated Microsoft Edge against actual Odoo on loopback, release/browser/edge.log. | 
| P05-AC-051 | Desktop and mobile usability | PARTIAL | Desktop flows and mobile overview width. Native mobile forms untested. | 
| P05-AC-052 | Theme verification | NOT_RUN | Theme variants unverified. | 
| P05-AC-053 | End-to-end performance | PARTIAL | 50-instrument ORM benchmark. Large portfolio and acquisition paths unprofiled. | 
| P05-AC-054 | Resource-pressure handling | PARTIAL | Explicit bounded tasks and bars. Controlled pressure testing open. | 
| P05-AC-055 | Security regression | PARTIAL | Role, company, provider isolation and allowlist tests. Security stress matrix open. | 
| P05-AC-056 | Company isolation | PASSED | Active company lookups and cross-company rejection verified with real ORM. | 
| P05-AC-057 | Real-order prohibition | PASSED | Fixed read-only operations and source scan, security/source.log. | 
| P05-AC-058 | Fresh installation | PASSED | Fresh Odoo installation and ORM regression, release/installation/fresh.log. | 
| P05-AC-059 | Populated P04 upgrade | PASSED | Populated P04 upgrade with unchanged record hashes and XML IDs. | 
| P05-AC-060 | Complete evidence-backed handoff | PASSED | Sanitized ZIP, checksum and full report/evidence manifests verified. | 

## 14 — Financial research results

The deterministic fixture starts with ₹50,000 virtual cash and ends with ₹49875.96. Gross is ₹-120, fees ₹4.04 and net ₹-124.04. Two synthetic fills close through stop-first handling. An aggregate risk veto blocks the third candidate under the fixture's 0.26% daily risk budget. The arithmetic checks software behavior under hypothetical fees. Real-market validation remains open. [Reproducible portfolio](docs/evidence/p05/portfolio/fixture.json)

## 15 — Performance results

The migrated disposable database processed 3,750 synthetic bars across 50 instruments. Wall time measured 4.45 s, maximum sampled process memory reached 141.1 MiB and the company count query took 1.3 ms. This benchmark measures ingestion and historical research. Queue throughput and max-capacity portfolio latency remain unmeasured. [Benchmark](docs/evidence/p05/upgrade-final/performance/orm.json)

## 16 — Security verification

Odoo verifies viewer, analyst and administrator paths, immutable portfolios, active-company datasets and provider-origin restrictions. The provider operations are allowlisted. Independent database connections contended for the local operation budgets. Sensitive runtime directories are excluded from the handoff, and the archive was checked for known secret patterns. [Source scan](docs/evidence/p05/security/source.log) · [Quota evidence](docs/evidence/p05/security/quota.log)

## 17 — Errors and bug fixes

The first portfolio fixture budget allowed all three candidates. The reproducible veto fixture now explicitly uses a stricter policy and verifies independent cash arithmetic. Two intermediate ORM runs caught malformed test syntax and a stale alias to the session cache. The corrected diagnostics test verifies that history cannot reuse a session after authorization is disabled and restored. [Issue register](docs/P05_REVIEW_ISSUES.md)

## 18 — Incomplete features

Open work includes authorized history and documented publication eligibility, account-wide quotas, instrument master ingestion, streaming, persistent single-use holdout, formal statistical evaluation, full indicator references, ST-04, ST-06, per-strategy execution coverage, ranking, background restart leases, additional dashboard work and pressure tests.

## 19 — Development completion metrics

Of the 60 P05 acceptance criteria, 18 passed within their stated scope, 33 are partial, 2 are externally blocked and 7 remain open without executed verification. The synthetic evidence establishes software behavior.

## 20 — Next development recommendations

Implement durable sealed holdout consumption and verify operator interruption and cross-plan contention on disposable databases. Verify one owner-authorized historical session before broadening acquisition. Extend independent portfolio metrics and per-strategy execution scenarios.

## 21 — Owner setup instructions

The owner guide covers offline use, local read-only authorization, account entitlement, network and timestamp conditions, historical data authorization and fee evidence. [Owner guide](docs/OWNER_ACTION_REQUIRED.md)

## 22 — Final readiness decision

**FOUNDATION VERIFIED** for offline Odoo research, synthetic historical acquisition and bounded synthetic portfolio replay. P05 has open technical and external requirements. The application remains scoped to historical research and synthetic simulation.
