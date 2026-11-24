# Golok AI Trading Lab Pro — P09 development report

**P09 DEVELOPMENT PARTIAL — TECHNICAL OR EXTERNAL BLOCKERS REMAIN**

24 November 2026, Asia/Kolkata. P09 snapshot version 20.0.9.0.0 adds recurring fixture research, manually advanced prospective fixture accounts, synthetic performance reports, and embargoed walk-forward experiments. It keeps original P08 tables and scopes. The acceptance matrix has 35 PASSED, 13 PARTIAL, 2 BLOCKED.

## Verified work

| Area | Result |
| --- | --- |
| Offline research and historical replay | Both archived target policies reproduced exactly. Source permissions, holdout restrictions and P08 replay regression passed. |
| Continuous research | One phase summary remains per watch and phase. Newly visible completed candles schedule durable recurring research, and evidence carries the actual input SHA-256. |
| Prospective fixture paper | Risk manager can reserve, process an authored entry and exit, close or leave an unresolved fixture position. Duplicate entry and exit, account contention and interruption recovery exercised. |
| Capital protection | Opening ₹50,000, paise arithmetic, 0.5% planned risk, 1% daily limit, three entries, suspension after two losses and minimum 2:1 planned net sizing. |
| Financial metrics and validation | Versioned synthetic portfolio metrics, net expectancy and separate sampled drawdowns. Four authored walk-forward folds retain losing and winning trial evidence and enforce embargo dates. |
| Providers and genuine data | Upstox and FYERS documented no-static-IP market-data options in scope. No actual account or source authorization established, no genuine session acquired, no financial strategy validation and no verified prospective delayed or live data. |
| Native Odoo workspace | Fixture cycles, risk-managed fixture accounts and their journal, synthetic performance reports and walk-forward reports. |
| Release and recovery | 51 standalone, 23 Odoo tests on fresh installation, 23 on update and 19 Edge checks. Populated P08 clone retained 945 XML IDs and hashed historical rows. The 50-instrument synthetic ingestion and research benchmark took 4.11 seconds. |

## Readiness by capability

| Capability | Readiness |
| --- | --- |
| Offline research | Available for fixture and already authorized P08 inputs. |
| Continuous research cycles | Verified for recurring fixture checks. |
| Historical data authorization | Existing P08 permission controls passed regression. |
| Historical replay | Available under the P08 proof and permission checks. |
| Prospective fixture paper trading | Manually advanced authored scenarios verified. |
| Prospective genuine delayed-data simulation | Unavailable. |
| Prospective verified-live paper trading | Unavailable. |
| Financial metrics | Synthetic completed trades and end-of-day equity verified. Intraday marks unavailable. |
| Transaction-cost evidence | Official rates reviewed. Per-fill estimate reconciled. Account-specific cost validation remains pending. |
| Walk-forward validation | Synthetic rolling and expanding partitions, immutable trials and embargoed folds verified. |
| Strategy financial validation | Blocked pending genuine licensed data and sufficient independent evidence. |
| Portfolio risk protection | Single fixture account limits verified. Broader portfolio limits remain open. |
| Paper trading dashboard | Native fixture account and journal verified in Edge. |
| System recovery | Research lease recovery and committed-state rollback and retry tested. |
| Security | Company isolation and protected records verified in local regression. |
| Verified live market data | Unavailable. |
| Actionable live recommendations | NO TRADE. |

## Technical gates

| Gate | Result |
| --- | --- |
| A Continuous research | Fixture recurrence, idempotence and lock contention verified. Full missed interval tracking and sustained authorized feeds remain open. |
| B Prospective paper | Cash, state transitions and recovery pass on authored manual fixtures. Candidate-to-order conversion and continuous observation-driven execution remain open. |
| C Capital protection | Account control and suspension pass on test scenarios. Cross-instrument portfolio checks remain open. |
| D Financial intelligence | Completed-trade metrics and chronological experiment lineage pass on authored data. Complete marks, broad stress testing and promotion governance remain open. |
| E Operational UI | Fixture paper and synthetic metrics workspaces passed Edge. General risk and strategy workspaces remain open. |
| F Release | Fresh installation, populated upgrade, browser and checksummed handoff verified. |

The development ZIP and its two internal manifests contain the implemented source and actual test evidence. The original P08 review ZIP remains independently verifiable. No live recommendation or broker order feature is enabled. [Owner actions](docs/OWNER_ACTION_REQUIRED.md) · [Tests](docs/P09_TEST_EXECUTION_REPORT.md) · [Open scope](docs/P09_ISSUE_REGISTER.md)


## Acceptance

| ID | Requirement | Status | Verified scope or gap | Evidence |
| --- | --- | --- | --- | --- |
| P09-AC-001 | P08 baseline and manifests verified | PASSED | P08 ZIP checksum, CRC and both manifests checked. Source checkpoint frozen. | baseline.log |
| P09-AC-002 | Existing standalone regression executed | PASSED | 47 baseline and 51 current standalone tests passed. | baseline-unit.log · unit.log |
| P09-AC-003 | Prior identifiers and historical results preserved | PASSED | Prior matrix preserved verbatim. Populated P08 rows and XML IDs survived; target outputs reproduced. | baseline.log · migration-final/upgrade/retention.log |
| P09-AC-004 | Phase summaries separated from recurring research cycles | PASSED | One phase summary and independent observation cycles. | final/installation/fresh.log |
| P09-AC-005 | Multiple intraday cycles verified | PASSED | Multiple cycles produced distinct completed observation snapshots in one phase. | final/installation/fresh.log |
| P09-AC-006 | Unchanged observations cannot produce duplicate cycles | PASSED | Rechecking unchanged data and the same phase created no duplicate. | final/installation/fresh.log |
| P09-AC-007 | Newly available observations trigger appropriate research | PASSED | Imported new fixture observations scheduled the next cycle during checks. | final/installation/fresh.log |
| P09-AC-008 | Concurrent cycle execution protected | PASSED | Independent PostgreSQL scheduler skipped the locked watch, leaving one cycle. | final/security/contention.log |
| P09-AC-009 | Missed research and restart recovery verified | PARTIAL | Committed job recovery and bounded missed-cycle estimates verified. Full missed-slot journaling remains open. | final/security/contention.log |
| P09-AC-010 | Dataset fingerprints and candidate evidence verified | PASSED | Cycle candidate stores snapshot hash. New replay gates carry the immutable frozen observation hash. | final/installation/fresh.log |
| P09-AC-011 | Prospective virtual accounts implemented | PASSED | Persistent INR fixture account and separate whole-paise balances verified. | final/installation/fresh.log |
| P09-AC-012 | Simulation operating modes strictly separated | PASSED | Fixture accounts, historical replay and authorized historical simulation have separate scopes; live and delayed prospective modes remain unavailable. | final/installation/fresh.log |
| P09-AC-013 | Persistent candidate lifecycle implemented | PARTIAL | Immutable descriptive NO TRADE outcome exists. Full strategy candidate lifecycle remains open. | final/installation/fresh.log |
| P09-AC-014 | Virtual order lifecycle verified | PARTIAL | Authored reserve, open, close, cancel, and unresolved covered. Candidate-to-order and general event-driven transition remain open. | final/installation/fresh.log |
| P09-AC-015 | Atomic cash and risk reservation verified | PASSED | Server reserves cash and planned risk together with the journal inside an account lock. | final/security/contention.log |
| P09-AC-016 | Conservative entry simulation verified | PARTIAL | Authored fixed fixture entry with size and fee checks. General observation-driven execution remains open. | final/installation/fresh.log |
| P09-AC-017 | Stop-loss simulation verified | PARTIAL | Adverse authored scenario closes at its prior specified gap price. General bar-based stop processing remains open. | final/installation/fresh.log |
| P09-AC-018 | Target-exit simulation verified | PARTIAL | Authored target scenario closes and reconciles. General market-observation trigger remains open. | final/installation/fresh.log |
| P09-AC-019 | Cancellation and reservation release verified | PASSED | Pause cancels pending entry and releases reserved cash and risk. | final/installation/fresh.log |
| P09-AC-020 | Session cutoff and unresolved-position handling verified | PARTIAL | Pending order cancels after day changes. Missing exit becomes unresolved without pricing. Real session square-off remains open. | final/installation/fresh.log |
| P09-AC-021 | Virtual ledger reconciliation verified | PASSED | Append-only journal and exact paise reconciliation after state changes. | final/installation/fresh.log |
| P09-AC-022 | Duplicate event and duplicate fill protection verified | PASSED | Duplicate entry and exit are ignored and unique order events remain enforced. | final/security/contention.log |
| P09-AC-023 | True concurrent virtual cash reservation tested | PASSED | Independent reservation transactions contended for the same account. | final/security/contention.log |
| P09-AC-024 | True concurrent virtual position closure tested | PASSED | Independent exit workers left a single close. | final/security/contention.log |
| P09-AC-025 | Actual prospective worker interruption and recovery tested | PASSED | Separate Odoo fixture exit worker terminated after uncommitted writes; retry reconciled. | final/security/contention.log |
| P09-AC-026 | Owner-approved risk defaults preserved | PASSED | ₹50,000, 0.5% planned trade risk, 1% daily limit, three entries, two losses and 2:1 net sizing retained. | final/installation/fresh.log |
| P09-AC-027 | Aggregate portfolio risk veto verified | PARTIAL | Account-level cash, single exposure and aggregate reserve checks. Cross-instrument and sector limits remain open. | final/installation/fresh.log |
| P09-AC-028 | Daily loss and entry-count protection verified | PARTIAL | Daily threshold and count are enforced. Independent limit-edge tests are incomplete. | final/installation/fresh.log |
| P09-AC-029 | Consecutive-loss suspension verified | PASSED | Two consecutive scenario losses caused persistent risk suspension. | final/installation/fresh.log |
| P09-AC-030 | Paper kill switch and controlled resume verified | PASSED | Risk-manager pause, reservation release, controlled resume and audited operator. | final/installation/fresh.log |
| P09-AC-031 | Effective-dated cost evidence reviewed | PASSED | Dated NSE and published broker cost evidence with account-specific gaps. | ../../FINANCIAL_COST_MODEL_REPORT.md |
| P09-AC-032 | Independent cost calculations reconciled | PASSED | Decimal per-fill reference reconciled entry, exit, GST and final net. Contract-note rounding remains distinct. | unit.log |
| P09-AC-033 | Financial metrics engine verified | PARTIAL | Reusable versioned completed-trade metrics. Intraday exposure and risk ratios require mark series. | unit.log · final/browser/edge.log |
| P09-AC-034 | Net expectancy and zero-trade handling verified | PASSED | Breakeven and no-trade evidence with fees counted once. | unit.log |
| P09-AC-035 | Drawdown classifications verified | PASSED | Realized-trade and end-of-day equity drawdowns separated. Intraday marks unavailable. | unit.log |
| P09-AC-036 | Generalized multi-fold walk-forward verified | PASSED | Four chronological folds executed on authored sessions. Rolling and expanding windows verified. | unit.log · final/installation/fresh.log |
| P09-AC-037 | Persistent experiment and fold lineage verified | PASSED | Five immutable training trials per fold, result references and reproducible experiment hash persisted. | final/installation/fresh.log |
| P09-AC-038 | Parameter-selection contamination prevented | PASSED | Embargo, explicit dates, sealed-window rejection and selection before evaluation. | unit.log · final/installation/fresh.log |
| P09-AC-039 | Stress scenarios executed | PARTIAL | Doubled-cost case reconciled. Comprehensive market-regime, missed-entry and parameter stress remain open. | synthetic-stress.json |
| P09-AC-040 | Holdout and promotion governance verified | PARTIAL | Existing single-use holdout and concurrency verified. Multi-stage promotion workflow remains open. | final/security/contention.log |
| P09-AC-041 | Practical free-provider decision matrix completed | PASSED | Bounded provider matrix, hotspot-specific options and owner prerequisites documented. | ../../FREE_MARKET_DATA_PROVIDER_EVALUATION.md |
| P09-AC-042 | Genuine market-data smoke test passed or explicitly blocked | BLOCKED | Zero genuine sessions. Owner-approved data and verified applicable rights absent. | ../../HISTORICAL_DATA_VALIDATION_REPORT.md |
| P09-AC-043 | Genuine financial validation passed or explicitly blocked | BLOCKED | No genuine research, out-of-sample, cost and real prospective sample. | ../../P09_FINANCIAL_VALIDATION_REPORT.md |
| P09-AC-044 | Prospective paper portfolio workspace verified | PASSED | Fixture portfolio account, controls and journal executed through native Edge forms. | final/browser/edge.log |
| P09-AC-045 | Strategy performance and risk workspaces verified | PARTIAL | Native synthetic metrics and account-level risk controls. General strategy and cross-portfolio risk workspaces incomplete. | final/browser/edge.log |
| P09-AC-046 | Real browser workflows executed | PASSED | 19 actual Edge checks on a disposable Odoo database. | final/browser/edge.log |
| P09-AC-047 | Security, company isolation and real-order prohibition verified | PASSED | Company-scoped read ACLs, protected journal and no broker-order routes. | source-check.log · final/installation/fresh.log |
| P09-AC-048 | Fresh install and populated P08 upgrade verified | PASSED | Fresh and update passed. Populated P08 clone retained 945 XML IDs and checked rows. | final/installation · migration-final/upgrade |
| P09-AC-049 | Current traceability and Gujarati documentation delivered | PASSED | Prior trace rows preserved, current acceptance and Gujarati setup delivered. | ../../REQUIREMENTS_TRACEABILITY.md · ../../OWNER_SETUP_GUJARATI.md |
| P09-AC-050 | Final archive, manifests and SHA-256 verified | PASSED | ZIP CRC, entry manifests, checkpoint and external SHA-256 checked. | manifest.sha256 · source.sha256 |
