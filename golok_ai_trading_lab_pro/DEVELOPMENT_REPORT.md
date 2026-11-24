# Golok AI Trading Lab Pro — P08 development report

**P08 DEVELOPMENT PARTIAL — TECHNICAL OR EXTERNAL BLOCKERS REMAIN**

24 November 2026, Asia/Kolkata. P08.1 extends company-specific authorization, audited daily-file normalization and calendar-driven scheduling with Odoo holdout isolation and bounded historical report recovery.

## Baseline and actual execution

The P07 handoff passed CRC, both manifests and external SHA-256 verification. The archived release and matrix remain recoverable, all prior identifiers were retained, and both target-policy outcomes reproduced. Final P08 verification ran 46 standalone tests, 16 Odoo cases each on fresh and update, and 15 Edge scenarios. The populated P07 upgrade retained 802 XML IDs and earlier record hashes. The database benchmark processed 3,750 synthetic observations over 50 instruments in 8.91 seconds. [Execution report](docs/P08_TEST_EXECUTION_REPORT.md)

## Vertical slices

| Workstream | Verified software and scope |
| --- | --- |
| Authorization | Manual CSV requires an exact company-scoped upstream grant, bound to the dataset on creation. Descriptive research and queued jobs recheck authorization. Revocation, supersession, display restrictions and retention dates apply to covered models. Full nested export and retention deletion remain open. |
| Unified dataset | Legacy and targeted modern cash validators remain available. The daily normalization workflow binds audit, effective mapping, ISIN, calendar and receipt to candle datasets. The complete normalization sequence was exercised on authored legacy data. Modern fixture parsing has standalone checks. |
| Free source discovery | NSE documentation reviewed. Actual authorized market coverage is zero. No real data, subscription, trial or accounts used. |
| Automatic research | Native Odoo scheduled action processes bounded fixture watches at explicit session phases. The pre-market, intraday, post-market and closed-day cases execute, deduplicate and persist status. No live acquisition or daily paper execution activated. |
| Recovery | A subprocess was killed with an uncommitted claim and the Odoo queue produced exactly one result. A separate fixture test recovered a missed post-market report, preserved its original cutoff and verified duplicate prevention. The automatic lookback is seven calendar days. Durable leases remain open. |
| Replay | Holdout partitions are excluded from application candle and research access. The historical contract now simulates intraday fills on authored fixtures, separating close, publication and execution, and verifies frozen provenance and fees. Production Odoo remains synthetic. |
| Dashboard | Native research schedule controls and persisted Daily Research Operations are available. Edge confirmed the fixture label and NO TRADE status. The original nine-workspace scope remains broader. |

The authorization domain initially failed at install and later at a direct-record read because Odoo used a normalized search value and a separate record evaluator. The final implementation supplies both a searchable authorization expression and an equivalent computed record value. These failures and the final run are retained.

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
| Job recovery | Transaction-level process interruption and recovery verified. Durable state coverage remains partial. |
| Operational dashboard | Native persisted fixture operations verified in Edge |
| Financial validation | Not established |
| Prospective paper trading | Not established |
| Verified live market data | Unavailable |
| Actionable live recommendations | NO TRADE |

The fixture scheduler requires Odoo and the computer to be running. The package retains published P07 outcomes without rewriting historical records. See the detailed authorization, scheduler and replay reports for outstanding controls and tests.

## P08 acceptance

23 PASSED, 16 PARTIAL, 1 BLOCKED across 40 criteria.


| ID | Required outcome | Status | Verified scope and remaining work | Evidence below docs/evidence/p08 |
| --- | --- | --- | --- | --- |
| P08-AC-001 | P07 baseline and historical results preserved | PASSED | Archive and source SHA-256, historical reports, both strategy results reproduced. | baseline/verification.log |
| P08-AC-002 | Existing regression tests executed | PASSED | 46 standalone, 16 fresh, 16 update and 15 Edge scenarios. | unit.log · final/ |
| P08-AC-003 | All prior requirement identifiers preserved | PASSED | Prior row identities retained. Five old status rows updated with verified scope. | ../../REQUIREMENTS_TRACEABILITY.md |
| P08-AC-004 | Central purpose-specific authorization implemented | PARTIAL | Publisher-bound purpose checks for manual CSV, research and jobs. Full export and operation vocabulary remains open. | final/installation/fresh.log |
| P08-AC-005 | Existing dataset authorization lineage implemented | PARTIAL | New references persisted. Older unbound real inputs intentionally remain restricted. | migration-final/upgrade/retention.log |
| P08-AC-006 | Expired authorization blocks prohibited research | PASSED | A superseding expired grant blocks research and queued job execution. | final/installation/fresh.log |
| P08-AC-007 | Revoked authorization blocks prohibited operations | PARTIAL | Revocation action, supersession and bound read predicates implemented. Comprehensive active-revocation matrix open. | final/installation/fresh.log |
| P08-AC-008 | Unauthorized read and export paths protected | PARTIAL | Restricted candle search, direct snapshot read and market export exercised. Nested exports remain open. | final/installation/fresh.log |
| P08-AC-009 | Synthetic provenance controls verified | PARTIAL | Uploaded simulation data stays in simulation mode. Signed, generated provenance remains open. | unit.log |
| P08-AC-010 | Unified import-to-dataset pipeline implemented | PARTIAL | Legacy authored file reaches mapped dataset, normalized candle and authorized research. Actual market file pending. | final/installation/fresh.log |
| P08-AC-011 | Legacy daily import regression passed | PASSED | Legacy accepted, quarantined and idempotent retries passed. | final/installation/fresh.log |
| P08-AC-012 | UDiFF profile verified within documented scope | PARTIAL | Targeted UDiFF header and data validation passed with authored cases. Official-file comparison open. | unit.log |
| P08-AC-013 | Dataset revision and duplicate protection verified | PARTIAL | Daily audit and candle unique keys protect identical or conflicting inputs. Versioning across provider revisions remains open. | final/installation/fresh.log |
| P08-AC-014 | Multi-session completeness and quarantine verified | PARTIAL | Existing gap and quarantine regressions passed. Complete daily multi-session merge unverified. | final/installation/fresh.log |
| P08-AC-015 | Cross-source conflict eligibility integrated | PARTIAL | P07 standalone comparator retained. No automatic ingestion conflict gate. | unit.log |
| P08-AC-016 | Retention policy enforcement verified | PARTIAL | Retention dates block covered reads and operations. Physical deletion and dedicated deadline test open. | ../../P08_AUTHORIZATION_AND_DATASET_REPORT.md |
| P08-AC-017 | Practical free-data provider investigation completed | PASSED | NSE academic use restrictions and eligibility reviewed. | ../../FREE_MARKET_DATA_PROVIDER_EVALUATION.md |
| P08-AC-018 | Genuine authorized data smoke test passed or explicitly blocked | BLOCKED | Source-specific real rights unavailable. Zero genuine sessions acquired. | ../../HISTORICAL_DATA_VALIDATION_REPORT.md |
| P08-AC-019 | Generalized historical replay contract implemented | PARTIAL | Standalone intraday replay on authored contract fixtures. Production historical execution remains disabled. | unit.log |
| P08-AC-020 | Historical and synthetic replay eligibility separated | PASSED | Intake assessment distinguishes daily and intraday. Portfolio keeps its synthetic-only boundary. | unit.log |
| P08-AC-021 | Publication-time causality tests passed | PASSED | Strict publication-before-decision, missing and unverified evidence cases passed. | unit.log |
| P08-AC-022 | Application-level holdout isolation improved | PASSED | Application search, record reads and exports block sealed candles. Single-use consumption and holdout contention reran. | replay-contract/installation/fresh.log · replay-contract/security/contention.log |
| P08-AC-023 | G01–G14 protected evidence handling verified | PASSED | Gate veto and metadata poisoning regression. Scope is software-only. | unit.log |
| P08-AC-024 | Session-aware native scheduler implemented | PASSED | Native fixture cron, explicit exchange calendar and persisted operations. | final/installation/fresh.log |
| P08-AC-025 | Pre-market workflow tested | PASSED | Deterministic pre-market dispatch verified. | final/installation/fresh.log |
| P08-AC-026 | Intraday orchestration tested in explicit fixture mode | PASSED | Fixture intraday produced descriptive research and NO TRADE. | final/installation/fresh.log |
| P08-AC-027 | Post-market report workflow tested | PASSED | Post-market research and persisted report verified. | final/installation/fresh.log |
| P08-AC-028 | Closed-day and exceptional-session behavior tested | PARTIAL | Closed-day ORM and maintenance unit cases passed. Broader exception scenarios open. | unit.log · final/installation/fresh.log |
| P08-AC-029 | Durable job states implemented | PARTIAL | Persistent queued/completed/failed/blocked/cancelled. Durable lease states remain open. | ../../P08_SCHEDULER_AND_RECOVERY_REPORT.md |
| P08-AC-030 | True concurrent job claiming verified | PASSED | Independent client held row and the competing worker skipped it. | final/security/contention.log |
| P08-AC-031 | Retry and cancellation idempotency verified | PARTIAL | Phase deduplication, prior job cancellation and successful retry exercised. Full transition audit open. | final/installation/fresh.log · final/security/contention.log |
| P08-AC-032 | Actual forced process interruption and recovery verified | PASSED | Actual process kill with rolled-back mutation and one recovered result. | final/security/contention.log |
| P08-AC-033 | Missed-session recovery preserves historical classification | PASSED | Bounded post-market recovery tested. Keeps the original cutoff and creates one historical fixture report. | replay-contract/installation/fresh.log |
| P08-AC-034 | Authorization expiry between job creation and execution tested | PASSED | Job submitted with granted access. Superseded and expired rights caused a blocked execution. | final/installation/fresh.log |
| P08-AC-035 | Operational dashboard backed by actual database records | PASSED | Native database-backed research operations list verified. | final/browser/edge.log |
| P08-AC-036 | Persistent daily report and owner controls verified | PARTIAL | Persisted phase report and watch pause/manual controls present. Full owner operations not exercised. | final/browser/edge.log |
| P08-AC-037 | Security and financial-safety regression passed | PASSED | Covered ACL, source, paper, holdout and read-only boundaries passed. | final/ · source-check.log |
| P08-AC-038 | Fresh installation and populated P07 upgrade verified | PASSED | Disposable P08.1 fresh/follow-up update and populated P07 clone passed. | replay-contract/installation · migration-replay/ |
| P08-AC-039 | Current traceability and Gujarati documentation delivered | PASSED | Gujarati owner guide and current status reconciliation included. | ../../OWNER_SETUP_GUJARATI.md |
| P08-AC-040 | Final evidence package and SHA-256 independently verified | PASSED | CRC, source manifest, all entries and independent external digest checked. | manifest.sha256 · source.sha256 |
