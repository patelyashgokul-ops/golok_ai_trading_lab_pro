# Golok AI Trading Lab Pro — P08 development report

**P08 DEVELOPMENT PARTIAL — TECHNICAL OR EXTERNAL BLOCKERS REMAIN**

24 November 2026, Asia/Kolkata. P08.4 adds deterministic fixture generation alongside fixed-term retention, recursive export protections, persisted source comparison and durable job claims. It retains holdout isolation, historical-report recovery and fixture intraday replay.

## Baseline and actual execution

The P07 handoff passed CRC, both manifests and external SHA-256 verification. The archived release and matrix remain recoverable, all prior identifiers were retained, and both target-policy outcomes reproduced. P08.4 ran 47 standalone tests, 19 Odoo cases each on fresh and update, and 16 Edge scenarios. The populated P07 upgrade retained 802 XML IDs and earlier record hashes. The database benchmark processed 3,750 synthetic observations over 50 instruments in 4.42 seconds. [Execution report](docs/P08_TEST_EXECUTION_REPORT.md)

## Vertical slices

| Workstream | Verified software and scope |
| --- | --- |
| Authorization | Manual CSV requires an exact company-scoped upstream grant. Bound rights are rechecked for descriptive research and queued jobs. Active revocation, fixed-retention expiry and recursive export denial passed. Physical archive disposition requires actual source terms. |
| Unified dataset | Legacy and targeted UDiFF cash files normalize into the same mapped daily dataset. The workflow detects a missing middle session and verifies backfill without rewriting the older research snapshot. Scope is authored fixtures. |
| Fixture lineage | Only the server can declare generated provenance. The dataset records a reserved synthetic instrument, seed, generator version and hash. Generated observations are protected against ordinary import. |
| Source integrity | Operator-triggered comparison records equivalent OHLCV and lineage evidence. A material mismatch blocks the affected datasets from new use. Independent legitimate market sources remain unverified. |
| Free source discovery | NSE documentation reviewed. Actual authorized market coverage is zero. No real data, subscription, trial or accounts used. |
| Automatic research | Native Odoo scheduled action processes bounded fixture watches at explicit session phases. The pre-market, intraday, post-market and closed-day cases execute, deduplicate and persist status. No live acquisition or daily paper execution activated. |
| Recovery | The cron commits a bounded five-minute lease. Recovery after expiry rejects obsolete worker tokens. A subprocess interruption and the committed-state tests each recovered a single result. Missed post-market report recovery preserves the original cutoff within seven calendar days. |
| Replay | Holdout partitions are excluded from application candle and research access. The historical contract now simulates intraday fills on authored fixtures, separating close, publication and execution, and verifies frozen provenance and fees. Production Odoo remains synthetic. |
| Dashboard | Native research schedule controls and persisted Daily Research Operations are available. Edge confirmed the fixture label and NO TRADE status. The original nine-workspace scope remains broader. |

The authorization domain initially failed at install and later at a direct-record read because Odoo used a normalized search value and a separate record evaluator. The final implementation supplies both a searchable authorization expression and an equivalent computed record value. These failures and the final run are retained.

P08.3's first retry test found a stale ORM state after a privileged write. The retry and cancellation paths now invalidate the affected fields before returning. The failed test and passing rerun are included.

The 50-instrument reference benchmark measures the existing bounded ingestion and research route. Holdout checks and replay serialization add database work. Worst-case holdout cardinality and scheduler throughput remain unmeasured.

## Readiness

| Capability | Status |
| --- | --- |
| Offline research | Verified for the tested fixture paths |
| Unified dataset ingestion | Verified for the legacy synthetic end-to-end workflow. Other sources remain limited. |
| Authorization enforcement | Verified on covered dataset, research, queue, read and direct export paths |
| Historical replay technical readiness | Intake checks available. Production execution remains synthetic. |
| Actual authorized market acquisition | Blocked by missing specific use rights and real data |
| Session scheduler and automatic research | Fixture phase workflows verified |
| Job recovery | Transaction interruption, durable claim expiry, single result and stale-token rejection verified. |
| Operational dashboard | Native persisted fixture operations verified in Edge |
| Financial validation | Not established |
| Prospective paper trading | Not established |
| Verified live market data | Unavailable |
| Actionable live recommendations | NO TRADE |

The fixture scheduler requires Odoo and the computer to be running. The package retains published P07 outcomes without rewriting historical records. See the detailed authorization, scheduler and replay reports for outstanding controls and tests.

| Completion gate | Result |
| --- | --- |
| A Authorization | Covered publisher-bound research, active revocation, expiry and nested export passed. Old unbound datasets stay restricted. |
| B Unified pipeline | Passed on authored Legacy CM and UDiFF through gap detection and backfill in Odoo. |
| C Automatic research | Passed in fixture mode for pre-market, intraday and post-market. |
| D Recovery | Passed for database worker contention, forced process termination and committed lease recovery. |
| E Safe replay | Partial. Synthetic replay, publication causality and holdout controls passed. Authorized historical execution remains limited to the standalone fixture route. |
| F Release integrity | Fresh and populated upgrade, browser checks and manifest verification passed within the documented test scope. |

## P08 acceptance

35 PASSED, 4 PARTIAL, 1 BLOCKED across 40 criteria.


| ID | Required outcome | Status | Verified scope and remaining work | Evidence below docs/evidence/p08 |
| --- | --- | --- | --- | --- |
| P08-AC-001 | P07 baseline and historical results preserved | PASSED | Archive and source SHA-256, historical reports, both strategy results reproduced. | baseline/verification.log |
| P08-AC-002 | Existing regression tests executed | PASSED | 47 standalone, 19 fresh, 19 update and 16 Edge scenarios. | unit.log · generated-fixture/ |
| P08-AC-003 | All prior requirement identifiers preserved | PASSED | Prior row identities retained. Five old status rows updated with verified scope. | ../../REQUIREMENTS_TRACEABILITY.md |
| P08-AC-004 | Central purpose-specific authorization implemented | PARTIAL | Publisher-bound purpose checks for manual CSV, research and jobs. Full export and operation vocabulary remains open. | generated-fixture/installation/fresh.log |
| P08-AC-005 | Existing dataset authorization lineage implemented | PARTIAL | New references persisted. Older unbound real inputs intentionally remain restricted. | migration-fixture/upgrade/retention.log |
| P08-AC-006 | Expired authorization blocks prohibited research | PASSED | A superseding expired grant blocks research and queued job execution. | generated-fixture/installation/fresh.log |
| P08-AC-007 | Revoked authorization blocks prohibited operations | PASSED | An active grant was revoked. Subsequent research and snapshot reads were denied. | generated-fixture/installation/fresh.log |
| P08-AC-008 | Unauthorized read and export paths protected | PASSED | Restricted search, read, nested market export and direct export with base Odoo privilege verified. | generated-fixture/installation/fresh.log |
| P08-AC-009 | Synthetic provenance controls verified | PASSED | Reserved instrument, deterministic generation, immutable fingerprint, duplicate generation and provenance forgery tested. | generated-fixture/installation/fresh.log · generated-fixture/browser/edge.log |
| P08-AC-010 | Unified import-to-dataset pipeline implemented | PASSED | Legacy and targeted UDiFF fixtures reached the same mapped daily dataset and authorized fixture research. | generated-fixture/installation/fresh.log |
| P08-AC-011 | Legacy daily import regression passed | PASSED | Legacy accepted, quarantined and idempotent retries passed. | generated-fixture/installation/fresh.log |
| P08-AC-012 | UDiFF profile verified within documented scope | PASSED | Targeted UDiFF profile parsed and normalized in Odoo with authored fixtures. Official market file verification remains external. | unit.log |
| P08-AC-013 | Dataset revision and duplicate protection verified | PARTIAL | Daily audit and candle unique keys protect identical or conflicting inputs. Versioning across provider revisions remains open. | generated-fixture/installation/fresh.log |
| P08-AC-014 | Multi-session completeness and quarantine verified | PASSED | Mixed-format daily normalization detected a missing middle session. Backfill produced a new complete snapshot and retained the old gap audit. | generated-fixture/installation/fresh.log |
| P08-AC-015 | Cross-source conflict eligibility integrated | PASSED | A persisted OHLCV mismatch blocked both mapped fixture datasets from new research. Operator-triggered. | generated-fixture/installation/fresh.log |
| P08-AC-016 | Retention policy enforcement verified | PASSED | Fixed-term expiry blocked reads and imports. Transient-only denied persistence. Protected rows remained intact. | ../../P08_AUTHORIZATION_AND_DATASET_REPORT.md |
| P08-AC-017 | Practical free-data provider investigation completed | PASSED | NSE academic use restrictions and eligibility reviewed. | ../../FREE_MARKET_DATA_PROVIDER_EVALUATION.md |
| P08-AC-018 | Genuine authorized data smoke test passed or explicitly blocked | BLOCKED | Source-specific real rights unavailable. Zero genuine sessions acquired. | ../../HISTORICAL_DATA_VALIDATION_REPORT.md |
| P08-AC-019 | Generalized historical replay contract implemented | PARTIAL | Standalone intraday replay on authored contract fixtures. Production historical execution remains disabled. | unit.log |
| P08-AC-020 | Historical and synthetic replay eligibility separated | PASSED | Intake assessment distinguishes daily and intraday. Portfolio keeps its synthetic-only boundary. | unit.log |
| P08-AC-021 | Publication-time causality tests passed | PASSED | Strict publication-before-decision, missing and unverified evidence cases passed. | unit.log |
| P08-AC-022 | Application-level holdout isolation improved | PASSED | Application search, record reads and exports block sealed candles. Single-use consumption and holdout contention reran. | generated-fixture/installation/fresh.log · generated-fixture/security/contention.log |
| P08-AC-023 | G01–G14 protected evidence handling verified | PASSED | Gate veto and metadata poisoning regression. Scope is software-only. | unit.log |
| P08-AC-024 | Session-aware native scheduler implemented | PASSED | Native fixture cron, explicit exchange calendar and persisted operations. | generated-fixture/installation/fresh.log |
| P08-AC-025 | Pre-market workflow tested | PASSED | Deterministic pre-market dispatch verified. | generated-fixture/installation/fresh.log |
| P08-AC-026 | Intraday orchestration tested in explicit fixture mode | PASSED | Fixture intraday produced descriptive research and NO TRADE. | generated-fixture/installation/fresh.log |
| P08-AC-027 | Post-market report workflow tested | PASSED | Post-market research and persisted report verified. | generated-fixture/installation/fresh.log |
| P08-AC-028 | Closed-day and exceptional-session behavior tested | PASSED | Closed day and maintenance between exceptional split sessions verified through Odoo. | generated-fixture/installation/fresh.log |
| P08-AC-029 | Durable job states implemented | PASSED | Committed claim, lease expiry, attempt bound, worker token and terminal state verified. | ../../P08_SCHEDULER_AND_RECOVERY_REPORT.md |
| P08-AC-030 | True concurrent job claiming verified | PASSED | Independent client held row and the competing worker skipped it. | generated-fixture/security/contention.log |
| P08-AC-031 | Retry and cancellation idempotency verified | PASSED | Repeated retry and cancellation preserve the same request. Recovery produces one result. | generated-fixture/installation/fresh.log · generated-fixture/security/contention.log |
| P08-AC-032 | Actual forced process interruption and recovery verified | PASSED | Actual process kill with rolled-back mutation and one recovered result. | generated-fixture/security/contention.log |
| P08-AC-033 | Missed-session recovery preserves historical classification | PASSED | Bounded post-market recovery tested. Keeps the original cutoff and creates one historical fixture report. | generated-fixture/installation/fresh.log |
| P08-AC-034 | Authorization expiry between job creation and execution tested | PASSED | Job submitted with granted access. Superseded and expired rights caused a blocked execution. | generated-fixture/installation/fresh.log |
| P08-AC-035 | Operational dashboard backed by actual database records | PASSED | Native database-backed research operations list verified. | generated-fixture/browser/edge.log |
| P08-AC-036 | Persistent daily report and owner controls verified | PASSED | Administrator role, manual check, pause/resume and idempotent phase reports verified. | generated-fixture/installation/fresh.log · generated-fixture/browser/edge.log |
| P08-AC-037 | Security and financial-safety regression passed | PASSED | Covered ACL, source, paper, holdout and read-only boundaries passed. | generated-fixture/ · source-check.log |
| P08-AC-038 | Fresh installation and populated P07 upgrade verified | PASSED | Disposable P08.4 fresh/follow-up update and populated P07 clone passed. | generated-fixture/installation · migration-fixture/ |
| P08-AC-039 | Current traceability and Gujarati documentation delivered | PASSED | Gujarati owner guide and current status reconciliation included. | ../../OWNER_SETUP_GUJARATI.md |
| P08-AC-040 | Final evidence package and SHA-256 independently verified | PASSED | CRC, source manifest, all entries and independent external digest checked. | manifest.sha256 · source.sha256 |
