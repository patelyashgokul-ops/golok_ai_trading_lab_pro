# Golok AI Trading Lab Pro — P06P07-R01 development report

**P06–P07 REPAIR PARTIAL — TECHNICAL OR EXTERNAL BLOCKERS REMAIN**

Release `20.0.9.1.1` starts from verified P09.1 release `20.0.9.1.0`. P09.1 archive, requirement identifiers, source checkpoint and prior published outputs were retained.

## Implemented

- Upstox V3 read-only historical acquisition for one closed NSE cash-equity session. Odoo uses the existing company-grant, reviewed calendar, instrument mapping, quota, validation and audit workflow. The injected fixture path has no account dependency.
- Automatic equivalent-candle comparison between Upstox and SmartAPI historical sync datasets. The Odoo regression verified a material difference, durable audit records and both dataset vetoes.
- Versioned causal entry and stop experiments with tick-aligned levels, liquidity, cost-aware sizing and expiry. An optional ATR-capped target policy is available in the historical portfolio wizard. The structure and fixed 4R baselines reproduced.
- The handoff reconciles all 180 P06 and P07 criteria and reviews the 97 original unresolved entries and 18 original defects. The 45 focused repair criteria are appended to traceability.

## Verification

58 standalone tests passed. The fresh Odoo installation and module-update stages each reported 25 tests with zero failures and errors. Independent PostgreSQL contention and actual worker termination/recovery scenarios passed. Edge ran 20 browser scenarios. The populated P09.1 upgrade preserved 1,243 existing XML IDs and record-level digests. All eleven archived P09.1 stress cases matched.

## Readiness

| Area | Disposition |
|---|---|
| Provider architecture | Upstox and SmartAPI historical fixture scope verified. Unified operational and provider health scope partial. |
| Authorized provider connectivity and genuine data | Blocked by verified entitlement and use rights. Zero genuine sessions. |
| Data accuracy protection | Equivalent broker sync comparison and material-conflict veto verified on fixtures. Adjustment and import-route coverage partial. |
| Entry and stop optimization | Causal standalone evaluator verified. Shared deployment and training excursion evidence partial. |
| Target optimization | Optional historical ATR policy verified. Training calibration partial. |
| Strategy competition | Historical ranking across five strategies verified. Cross-instrument prospective competition partial. |
| Research and parameter optimization | Existing snapshot findings and separated walk-forward workflow retained. Standardized RE coverage and broad train-only policy search partial. |
| Automatic research and fixture paper | Local scheduler, candidates, capital and journal regressions passed. |
| Genuine prospective paper and independent financial validation | Blocked by genuine data/use rights, independent evaluation and real cost evidence. |
| Verified live feed and actionable live support | Disabled pending separately authorized and validated evidence. |

P10 was not started.

[Completion matrix](docs/P06_P07_COMPLETION_MATRIX.md) · [Issue register](docs/P06_P07_ISSUE_REGISTER.md) · [Test report](docs/P06_P07_TEST_EXECUTION_REPORT.md) · [Owner steps](docs/OWNER_ACTION_REQUIRED.md)
