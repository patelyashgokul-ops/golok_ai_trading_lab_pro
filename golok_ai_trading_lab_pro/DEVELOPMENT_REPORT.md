# Golok AI Trading Lab Pro — P06P07-R01 development report

**P06–P07 REPAIR PARTIAL — TECHNICAL OR EXTERNAL BLOCKERS REMAIN**

Release `20.0.9.1.11` continues P06P07-R01 from verified P09.1 release `20.0.9.1.0`. The P09.1 archive, requirement identifiers, source checkpoint and prior published outputs were retained.

## Implemented

- Upstox V3 read-only historical acquisition for one closed NSE cash-equity session. Both the direct sync wizard and the operator-run sync plan use the provider-specific grant, reviewed calendar, instrument mapping, quota, validation and audit workflow. The injected fixture path has no account dependency.
- One automatic comparison service covers eligible Upstox, SmartAPI, Bhavcopy and administrator-attested local CSV intake. Material disagreement blocks both datasets, possible corporate-action mismatches are recorded and a replacement requires an independent corroborating observation.
- The **Experimental causal entry, stop and target** policy connects the evaluator to historical portfolio replay. It freezes proposed levels and expiry before checking the next eligible open. Selecting this policy in the walk-forward wizard trains on 20 strategy–policy combinations per fold and carries the selected pair into validation and evaluation. The structure and fixed 4R baselines reproduced.
- **Provider Diagnostics** includes a local Upstox readiness check that reports setup, review status and genuine historical receipts separately.
- Prospective fixture competition compares due instruments at an exact cutoff using the historical portfolio's cost-aware rank. A bound account can evaluate all five strategy definitions. A job cannot allocate capital after the cohort deadline, and one eligible winner can reserve the account's virtual capital.
- **Fixture Candidate Research** exposes levels, expiry, ranking and gate outcomes. **Review Provider Status** exposes current company source rights, retention, quotas, historical receipts and links to source records.
- A walk-forward run can fit a conservative target cap from completed training trades. The versioned snapshot evidence contract covers the original 25 identifiers and adds a descriptive historical-pattern outcome counter.
- Overview counters and drill-down lists share a server-side company and access scope. New cards expose fixture accounts and candidates, strategy performance records and daily research events.
- The historical sync wizard can try one independently approved alternate broker mapping for the same instrument and session after a transient primary-provider failure. Each attempt has its own linked audit record.
- G01–G14 decisions record typed evidence and SHA-256 fingerprints of the dataset and observations used. Malformed evidence and failed gates prevent allocation.
- A sealed holdout protects the date window across source aliases, research jobs, comparison records and prospective observations. A pending job cannot release evidence after sealing. The risk reviewer can consume the holdout once.
- Provider Diagnostics reports the seven separate historical acquisition capability states. A recorded historical receipt represents evidence for its own session. Current production connectivity and data quality remain unverified.
- Fixture candidates keep the observation, availability, local receipt, cutoff and expiry together. A completed entry bar outside a frozen experimental range invalidates the pending candidate and releases virtual capital.
- Historical and prospective competition records identify the shared ranking version and explicitly leave unmeasured financial inputs unknown.
- The chart opens from the selected research snapshot and uses its verified input window for OHLC, EMA 20, SMA 20 and VWAP where available. The dashboard gap register covers all nine workspaces.
- Daily Research Operations opens a company-scoped session report based on persisted phase, candidate, synchronization and paper-order records. It shows covered observations, recorded strategies, candidate reasons, risk vetoes and realized fixture results. The risk list exposes daily realized net and optional opening, reservation and position-cost balances.
- Market Data API Configuration adds a disabled-by-default Upstox selection, Windows DPAPI credential entry and rotation, a permission-gated read-only connection check, separate history and instrument-reference status, automatic historical plan advancement and optional descriptive research scheduling.
- The optional Upstox V3 worker processes repeated eligible LTPC updates, renews bounded connections and stores deduplicated private observations. Direct strategy, point-in-time replay and prospective paper handoff remain incomplete. Genuine provider and financial evidence remain blocked. [Configuration and coverage](docs/UPSTOX_ANALYTICS_CONFIGURATION.md)
- Upstox instrument synchronization saves the bounded NSE cash-equity catalog under the company's current source review. Identical content is reused and changed content receives a new SHA-256 revision. The imported catalog is searchable and remains separate from reviewed instrument mappings.
- The Historical Stock Scanner adds timeframe, sector and quality filters plus stored momentum, relative volume and trend evidence. Earlier snapshots can display a blank where the corresponding evidence was unavailable.
- Synthetic strategy performance reports chart saved end-of-day equity and drawdown and expose the exact dated numbers. The replay's opening balance is included in the drawdown peak calculation.
- The handoff reconciles all 180 P06 and P07 criteria and reviews the 97 original unresolved entries and 18 original defects. The 45 focused repair criteria are appended to traceability.

## Verification

72 standalone tests passed. Fresh Odoo installation and module update each passed 28 tests. Edge passed 29 checks, including the daily portfolio curves. Independent PostgreSQL contention, worker termination and recovery passed. The dedicated worker lease excludes a second worker in the same company. Populated upgrades preserved 1,243 XML IDs from P09.1 and 1,388 from the preceding R01 database, along with the compared historical record digests. All eleven archived P09.1 stress cases matched. Of the original 45 focused repair criteria, 41 passed and four remain partial. The Upstox addendum has separate traceability.

## Readiness

| Area | Disposition |
|---|---|
| Provider architecture | Upstox and SmartAPI historical fixture acquisition and one reviewed alternate verified. Unified operational and provider health scope partial. |
| Authorized provider connectivity and genuine data | Blocked by verified entitlement and use rights. Zero genuine sessions. |
| Data accuracy protection | The required negative fixture cases ran. Broker history, authorized raw daily file and attested CSV routes compare equivalent observations and require corroborated replacement. Independent authorized observations remain outstanding. |
| Entry and stop optimization | Causal historical portfolio integration verified with frozen proposals and no-trade vetoes. Prospective coverage and training excursion evidence remain open. |
| Target optimization | Optional historical ATR policy verified. Training calibration partial. |
| Strategy competition | Historical and prospective fixture ranking share the cost-aware score. Genuine statistical ranking and broader strategy validation remain open. |
| Research and parameter optimization | Twenty baseline configurations and optional fitted target variants use separate training, validation and evaluation. Versioned snapshot results identify implemented computations and missing or specialized inputs. |
| Automatic research and fixture paper | Local scheduler, candidates, capital and journal regressions passed. |
| Genuine prospective paper and independent financial validation | Blocked by genuine data/use rights, independent evaluation and real cost evidence. |
| Verified live feed and actionable live support | Disabled pending separately authorized and validated evidence. |

P10 was not started.

[Completion matrix](docs/P06_P07_COMPLETION_MATRIX.md) · [Issue register](docs/P06_P07_ISSUE_REGISTER.md) · [Dashboard reconciliation](docs/DASHBOARD_KPI_DEFINITIONS.md) · [Test report](docs/P06_P07_TEST_EXECUTION_REPORT.md) · [Owner steps](docs/OWNER_ACTION_REQUIRED.md)
