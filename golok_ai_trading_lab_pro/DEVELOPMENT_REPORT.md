# Golok AI Trading Lab Pro — P09.1 development report

**P09 TECHNICAL DEVELOPMENT COMPLETE — READY FOR P10 REVIEW**

24 November 2026, Asia/Kolkata. This revision adds automatic prospective fixture execution, shared simulated risk, restart interval logging, frozen close-mark metrics and a promotion evidence review. The acceptance matrix records 48 PASSED, 0 PARTIAL, 2 BLOCKED. The original P09 source and reports are archived inside the handoff.

| Capability | Verified result |
| --- | --- |
| Offline research and authorized historical replay | Existing P08 source authorization, frozen replay and holdout behavior passed regression. |
| Continuous research | Unique recurring cycles remain separate from phase summaries. Missed operating intervals now persist with actual resume time. |
| Prospective fixture paper | Strategy findings reserve cash and risk atomically. Later eligible candles advance the simulated position. A missing cutoff observation keeps the position unresolved. |
| Prospective genuine delayed or live paper | Blocked for lack of applicable feed access and permission. |
| Capital protection | Multiple schedules share INR 50,000 starting capital and a single exposure slot. Competing instruments cannot bypass the account budget. Daily loss, entry-count and kill-switch tests passed. |
| Financial metrics | Closed cash, end-of-day and visible frozen intraday marks are reported separately. Net expectancy uses completed outcomes after costs. Mark and ratio values are withheld when inputs are insufficient. |
| Transaction-cost evidence | Published NSE rates reviewed. An explicitly modeled per-fill case reconciles. Actual broker contract-note treatment remains unverified. |
| Walk-forward and stress | Frozen training trials and embargoed folds preserved. Eleven authored stress and baseline scenarios executed. |
| Strategy promotion | Synthetic experiments receive a blocked promotion evidence review. No strategy has genuine financial validation. |
| Native paper and strategy UI | Risk monitor, synthetic performance reports, fixture orders and journal verified in Edge. |
| Recovery and security | Independent workers, one fixture journal exit after interruption, protected financial records, company boundaries and read-only broker scope passed. |
| Verified market feed or actionable recommendation | Unavailable. All prospective outputs are fixture simulation only. |

## Evidence and remaining work

52 standalone tests passed. Odoo ran 24 cases each on fresh install and update, and Edge exercised 20 scenarios. The populated P08 clone upgraded directly. The initial P09 clone retained 1156 existing XML IDs and audited journal and snapshot hashes. The existing 50-instrument reference workload took 4.23 seconds on authored data.

The first automatic fixture test failed because Odoo held the original field-default callable for ingestion time. The import path now captures the server receipt explicitly in the ingestion transaction. The passing test uses the same clock for import and scheduling. Stored historical receipt values remain intact.

The candidate lifecycle distinguishes experiment, watch, risk rejection, expiry, invalidation, waiting and actual fixture exposure. The interruption harness terminated an Odoo process after an observation-driven exit had been written but before it committed. Retry posted exactly one exit. Genuine market-data verification and financial strategy validation require a licensed sample and documented rights. No broker was accessed and no genuine session was acquired. [Acceptance details](docs/REQUIREMENTS_TRACEABILITY.md) · [Owner actions](docs/OWNER_ACTION_REQUIRED.md) · [Tests](docs/P09_TEST_EXECUTION_REPORT.md)

| Mandatory gate | Verified scope |
| --- | --- |
| A Continuous research | Recurring cycles, unique observations, concurrent watch lock, elapsed intervals and durable queue restart. |
| B Prospective paper | Authored observation stream, candidate, reservation, entry, exit, reconciliation and uncommitted exit recovery. |
| C Capital protection | Shared-risk budget, concurrent cash reservation, daily and consecutive-loss limits, pause and resume. |
| D Financial intelligence | Independent Decimal reconciliation, zero-trade status, sampled equity and walk-forward isolation. |
| E Operational UI | Native journal, account risk monitor, strategy reports and fixture and historical scope. |
| F Release | Fresh install, populated P08 upgrade, Edge execution and verified handoff. |


## Acceptance

| ID | Requirement | Status | Verified scope or gap | Evidence |
| --- | --- | --- | --- | --- |
| P09-AC-001 | P08 baseline and manifests verified | PASSED | P08 ZIP checksum, CRC and both manifests checked. Source checkpoint frozen. | baseline.log |
| P09-AC-002 | Existing standalone regression executed | PASSED | 47 baseline and 52 current standalone tests passed. | baseline-unit.log · paper-unit.log |
| P09-AC-003 | Prior identifiers and historical results preserved | PASSED | Prior matrix preserved verbatim. Populated P08 rows and XML IDs survived; target outputs reproduced. | baseline.log · migration-final/upgrade/retention.log |
| P09-AC-004 | Phase summaries separated from recurring research cycles | PASSED | One phase summary and independent observation cycles. | lifecycle-final/installation/fresh.log |
| P09-AC-005 | Multiple intraday cycles verified | PASSED | Multiple cycles produced distinct completed observation snapshots in one phase. | lifecycle-final/installation/fresh.log |
| P09-AC-006 | Unchanged observations cannot produce duplicate cycles | PASSED | Rechecking unchanged data and the same phase created no duplicate. | lifecycle-final/installation/fresh.log |
| P09-AC-007 | Newly available observations trigger appropriate research | PASSED | Imported new fixture observations scheduled the next cycle during checks. | lifecycle-final/installation/fresh.log |
| P09-AC-008 | Concurrent cycle execution protected | PASSED | Independent PostgreSQL scheduler skipped the locked watch, leaving one cycle. | lifecycle-final/security/contention.log |
| P09-AC-009 | Missed research and restart recovery verified | PASSED | Persisted elapsed missed intervals without backdated signals. Existing history and durable lease recovery reran. | lifecycle-final/installation/fresh.log · lifecycle-final/security/contention.log |
| P09-AC-010 | Dataset fingerprints and candidate evidence verified | PASSED | Cycle candidate stores snapshot hash. New replay gates carry the immutable frozen observation hash. | lifecycle-final/installation/fresh.log |
| P09-AC-011 | Prospective virtual accounts implemented | PASSED | Persistent INR fixture account and separate whole-paise balances verified. | lifecycle-final/installation/fresh.log |
| P09-AC-012 | Simulation operating modes strictly separated | PASSED | Fixture accounts, historical replay and authorized historical simulation have separate scopes; live and delayed prospective modes remain unavailable. | lifecycle-final/installation/fresh.log |
| P09-AC-013 | Persistent candidate lifecycle implemented | PASSED | Immutable candidate evidence, experimental, risk-rejected, paper and expired states persisted. Waiting, invalidation and unresolved cases have distinct reasons. | lifecycle-final/installation/fresh.log |
| P09-AC-014 | Virtual order lifecycle verified | PASSED | Eligible research candidate generated and reserved one order, then lifecycle advanced with observed candles. | lifecycle-final/installation/fresh.log |
| P09-AC-015 | Atomic cash and risk reservation verified | PASSED | Server reserves cash and planned risk together with the journal inside an account lock. | lifecycle-final/security/contention.log |
| P09-AC-016 | Conservative entry simulation verified | PASSED | Strictly later opening, received-bar, limit and liquidity checks verified. | paper-unit.log · lifecycle-final/installation/fresh.log |
| P09-AC-017 | Stop-loss simulation verified | PASSED | Stop-first ambiguity, gap-open policy and entry-bar conservatism exercised in authored tests. | paper-unit.log · lifecycle-final/installation/fresh.log |
| P09-AC-018 | Target-exit simulation verified | PASSED | A later observation caused the target exit, exactly one close and reconciled cash. | lifecycle-final/installation/fresh.log |
| P09-AC-019 | Cancellation and reservation release verified | PASSED | Pause cancels pending entry and releases reserved cash and risk. | lifecycle-final/installation/fresh.log |
| P09-AC-020 | Session cutoff and unresolved-position handling verified | PASSED | Cutoff policy and unresolved treatment verified. No closing price was invented when no cutoff observation was received. | lifecycle-final/installation/fresh.log |
| P09-AC-021 | Virtual ledger reconciliation verified | PASSED | Append-only journal and exact paise reconciliation after state changes. | lifecycle-final/installation/fresh.log |
| P09-AC-022 | Duplicate event and duplicate fill protection verified | PASSED | Duplicate entry and exit are ignored and unique order events remain enforced. | lifecycle-final/security/contention.log |
| P09-AC-023 | True concurrent virtual cash reservation tested | PASSED | Independent reservation transactions contended for the same account. | lifecycle-final/security/contention.log |
| P09-AC-024 | True concurrent virtual position closure tested | PASSED | Independent exit workers left a single close. | lifecycle-final/security/contention.log |
| P09-AC-025 | Actual prospective worker interruption and recovery tested | PASSED | Separate Odoo workers were terminated after uncommitted manual and observation-driven exit writes. Each retry posted one exit. | lifecycle-final/security/contention.log |
| P09-AC-026 | Owner-approved risk defaults preserved | PASSED | ₹50,000, 0.5% planned trade risk, 1% daily limit, three entries, two losses and 2:1 net sizing retained. | lifecycle-final/installation/fresh.log |
| P09-AC-027 | Aggregate portfolio risk veto verified | PASSED | Competing fixtures from separate instruments share one capital balance, risk budget and exposure slot. | lifecycle-final/installation/fresh.log |
| P09-AC-028 | Daily loss and entry-count protection verified | PASSED | A fourth daily entry was refused and a severe gap independently triggered the daily loss suspension. | lifecycle-final/installation/fresh.log |
| P09-AC-029 | Consecutive-loss suspension verified | PASSED | Two consecutive scenario losses caused persistent risk suspension. | lifecycle-final/installation/fresh.log |
| P09-AC-030 | Paper kill switch and controlled resume verified | PASSED | Risk-manager pause, reservation release, controlled resume and audited operator. | lifecycle-final/installation/fresh.log |
| P09-AC-031 | Effective-dated cost evidence reviewed | PASSED | Dated NSE and published broker cost evidence with account-specific gaps. | ../../FINANCIAL_COST_MODEL_REPORT.md |
| P09-AC-032 | Independent cost calculations reconciled | PASSED | Decimal per-fill reference reconciled entry, exit, GST and final net. Contract-note rounding remains distinct. | unit.log |
| P09-AC-033 | Financial metrics engine verified | PASSED | Versioned exact financial metrics and frozen sampled intraday marks displayed. Unavailable inputs suppress unsupported statistics. | paper-unit.log · lifecycle-final/browser/edge.log |
| P09-AC-034 | Net expectancy and zero-trade handling verified | PASSED | Breakeven and no-trade evidence with fees counted once. | unit.log |
| P09-AC-035 | Drawdown classifications verified | PASSED | Closed cash, end-of-day and frozen sampled intraday mark-to-market drawdowns distinguished. | paper-unit.log · lifecycle-final/browser/edge.log |
| P09-AC-036 | Generalized multi-fold walk-forward verified | PASSED | Four chronological folds executed on authored sessions. Rolling and expanding windows verified. | unit.log · lifecycle-final/installation/fresh.log |
| P09-AC-037 | Persistent experiment and fold lineage verified | PASSED | Five immutable training trials per fold, result references and reproducible experiment hash persisted. | lifecycle-final/installation/fresh.log |
| P09-AC-038 | Parameter-selection contamination prevented | PASSED | Embargo, explicit dates, sealed-window rejection and selection before evaluation. | unit.log · lifecycle-final/installation/fresh.log |
| P09-AC-039 | Stress scenarios executed | PASSED | Eleven deterministic common-input stress and baseline cases executed with genuine regime validation left pending. | automatic-stress.json |
| P09-AC-040 | Holdout and promotion governance verified | PASSED | Single-use holdout enforced and fixture financial promotion explicitly blocked in a frozen risk review. | lifecycle-final/installation/fresh.log · lifecycle-final/security/contention.log |
| P09-AC-041 | Practical free-provider decision matrix completed | PASSED | Bounded provider matrix, hotspot-specific options and owner prerequisites documented. | ../../FREE_MARKET_DATA_PROVIDER_EVALUATION.md |
| P09-AC-042 | Genuine market-data smoke test passed or explicitly blocked | BLOCKED | Zero genuine sessions. Owner-approved data and verified applicable rights absent. | ../../HISTORICAL_DATA_VALIDATION_REPORT.md |
| P09-AC-043 | Genuine financial validation passed or explicitly blocked | BLOCKED | No genuine research, out-of-sample, cost and real prospective sample. | ../../P09_FINANCIAL_VALIDATION_REPORT.md |
| P09-AC-044 | Prospective paper portfolio workspace verified | PASSED | Fixture portfolio account, controls and journal executed through native Edge forms. | lifecycle-final/browser/edge.log |
| P09-AC-045 | Strategy performance and risk workspaces verified | PASSED | Native strategy metrics and fixture account-level risk monitor verified in Edge. | lifecycle-final/browser/edge.log |
| P09-AC-046 | Real browser workflows executed | PASSED | 20 actual Edge checks on a disposable Odoo database. | lifecycle-final/browser/edge.log |
| P09-AC-047 | Security, company isolation and real-order prohibition verified | PASSED | Company-scoped read ACLs, protected journal and no broker-order routes. | source-check.log · lifecycle-final/installation/fresh.log |
| P09-AC-048 | Fresh install and populated P08 upgrade verified | PASSED | Fresh and update passed. Populated P08 and P09 clones preserved prior XML IDs and stored results. Initial P09 retained 1156 IDs. | lifecycle-final/installation · direct-p08-migration/upgrade · lifecycle-migration/upgrade |
| P09-AC-049 | Current traceability and Gujarati documentation delivered | PASSED | Prior trace rows preserved, current acceptance and Gujarati setup delivered. | ../../REQUIREMENTS_TRACEABILITY.md · ../../OWNER_SETUP_GUJARATI.md |
| P09-AC-050 | Final archive, manifests and SHA-256 verified | PASSED | ZIP CRC, entry manifests, checkpoints and external SHA-256 checked. | manifest.sha256 · source.sha256 |
