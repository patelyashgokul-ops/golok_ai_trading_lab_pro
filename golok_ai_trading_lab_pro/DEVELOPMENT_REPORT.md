# Golok AI Trading Lab Pro — P06P07-R01 development report

**P06–P07 REPAIR PARTIAL — TECHNICAL OR EXTERNAL BLOCKERS REMAIN**

Release `20.0.9.1.4` continues P06P07-R01 from verified P09.1 release `20.0.9.1.0`. The P09.1 archive, requirement identifiers, source checkpoint and prior published outputs were retained.

## Implemented

- Upstox V3 read-only historical acquisition for one closed NSE cash-equity session. Both the direct sync wizard and the operator-run sync plan use the provider-specific grant, reviewed calendar, instrument mapping, quota, validation and audit workflow. The injected fixture path has no account dependency.
- One automatic comparison service covers eligible Upstox, SmartAPI, Bhavcopy and administrator-attested local CSV intake. Material disagreement blocks both datasets, possible corporate-action mismatches are recorded and a replacement requires an independent corroborating observation.
- The **Experimental causal entry, stop and target** policy connects the evaluator to historical portfolio replay. It freezes proposed levels and expiry before checking the next eligible open. Selecting this policy in the walk-forward wizard trains on 20 strategy–policy combinations per fold and carries the selected pair into validation and evaluation. The structure and fixed 4R baselines reproduced.
- **Provider Diagnostics** includes a local Upstox readiness check that reports setup, review status and genuine historical receipts separately.
- Prospective fixture competition compares due instruments at an exact cutoff using the historical portfolio's cost-aware rank. A bound account can evaluate all five strategy definitions. A job cannot allocate capital after the cohort deadline, and one eligible winner can reserve the account's virtual capital.
- **Fixture Candidate Research** exposes levels, expiry, ranking and gate outcomes. **Review Provider Status** exposes current company source rights, retention, quotas, historical receipts and links to source records.
- The handoff reconciles all 180 P06 and P07 criteria and reviews the 97 original unresolved entries and 18 original defects. The 45 focused repair criteria are appended to traceability.

## Verification

60 standalone tests passed. The fresh Odoo installation and module-update stages each passed 25 tests. Edge passed 23 checks, including Upstox readiness, provider status and the fixture candidate list. Independent PostgreSQL contention, worker termination and recovery passed. The populated upgrades from P09.1 and the previous R01 build retained existing XML IDs and record-level digests. All eleven archived P09.1 stress cases matched. Of the focused repair criteria, 30 passed and 15 remain partial.

## Readiness

| Area | Disposition |
|---|---|
| Provider architecture | Upstox and SmartAPI historical fixture scope verified. Unified operational and provider health scope partial. |
| Authorized provider connectivity and genuine data | Blocked by verified entitlement and use rights. Zero genuine sessions. |
| Data accuracy protection | Fixtures verify broker history, authorized raw daily file and attested CSV comparisons, possible split mismatches and corroborated replacement. Independent authorized observations remain outstanding. |
| Entry and stop optimization | Causal historical portfolio integration verified with frozen proposals and no-trade vetoes. Prospective coverage and training excursion evidence remain open. |
| Target optimization | Optional historical ATR policy verified. Training calibration partial. |
| Strategy competition | Historical and prospective fixture ranking share the cost-aware score. Genuine statistical ranking and broader strategy validation remain open. |
| Research and parameter optimization | Existing snapshot findings and separated walk-forward workflow retained. The historical train-only grid covers 20 pairs per fold. Broader parameter and standardized RE coverage remain open. |
| Automatic research and fixture paper | Local scheduler, candidates, capital and journal regressions passed. |
| Genuine prospective paper and independent financial validation | Blocked by genuine data/use rights, independent evaluation and real cost evidence. |
| Verified live feed and actionable live support | Disabled pending separately authorized and validated evidence. |

P10 was not started.

[Completion matrix](docs/P06_P07_COMPLETION_MATRIX.md) · [Issue register](docs/P06_P07_ISSUE_REGISTER.md) · [Test report](docs/P06_P07_TEST_EXECUTION_REPORT.md) · [Owner steps](docs/OWNER_ACTION_REQUIRED.md)
