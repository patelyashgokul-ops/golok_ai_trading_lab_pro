# P06–P07 test execution

| Verification | Command or entry point | Observed outcome |
|---|---|---|
| P09.1 baseline | Archive SHA-256, CRC, full and source manifests, source and report parity | 668 archived entries, 667 full manifest entries and 95 source entries matched. The read-only source checkpoint was created. |
| Baseline and final standalone | `python -B -m unittest discover -s tests -p 'unit_*.py' -v` | 52 baseline and 58 final tests passed. |
| Runtime source checks | `python -B scripts/check_source.py` | 68 source files inspected, Python/XML syntax passed and prohibited order and literal credential patterns were absent. |
| P09.1 stress checksum | `scripts.reproduce_p09_stress.stress` | All eleven output scenarios matched their archived results. |
| Strategy and level policy comparison | `scripts.reproduce_p06.run` and the three policies through `services.portfolio.replay` | Five strategies reran. The common fixture produced zero structure trades, three fixed-4R fills with −₹186.06 net and zero ATR-capped trades. Reversing asset and policy input order preserved results. |
| Fresh Odoo and module update | `scripts/verify_odoo.ps1 -Browser` | 25 ORM tests reported with no failures or errors per stage. Includes Upstox fixture ingestion and automatic source conflict protection. |
| Populated upgrade | `scripts/verify_p01_upgrade.ps1 -SourceVersion 20.0.9.1.0 -TargetVersion 20.0.9.1.1` | Preserved 1,243 existing XML IDs, record-level table hashes and immutable snapshot digests on an independent clone. |
| PostgreSQL independent processes | `scripts/verify_contention.py` through the harness | Import, range exclusion, reserve, closure, holdout, scheduler and restart scenarios passed, including actual worker termination and exactly-once retry in test transactions. |
| Microsoft Edge | `scripts/verify_browser.py` through the harness | 20 existing browser scenarios passed. Screenshots are included. |
| Populated-clone performance | `scripts/measure_odoo_p02.py` through upgrade harness | 3,750 synthetic bars across 50 instruments, about 6.34 seconds total, and approximately 148 MB peak process RSS. |
| Offline Upstox performance | Injected V3 JSON with 50 complete 375-bar sessions | 18,750 observations. Approximately 5.38 seconds parsing and 4.18 seconds session validation with Python allocation tracking enabled. |
| Genuine provider and financial checks | No account request made | Unavailable without owner entitlement, an authorized sample and independent costs. |

The early numerical fixture run failed two tests because the adopted historical example contained too few bars for ATR warm-up. The corrected independent 18-bar fixture passed the complete standalone suite. Expected SQL rejection messages in ORM logs correspond to asserted uniqueness and exclusion tests.

## Release 20.0.9.1.2 follow-up

- The final standalone suite passed all 60 tests. The joint-policy regression exercised a valid fill and a shifted open that invalidated the fill without changing the underlying proposal. The expanded negative suite exercised identity, price, adjustment, stale and authorization cases.
- `python -B scripts/reproduce_p06.py --level-policies` reproduces the four-policy comparison, including proposals, fills and zero-trade results. Its reference sample produced three fixed-4R trades and zero trades for structure, ATR-capped and joint policies. A separate authored fixture exercised an actual joint-policy simulated fill.
- The Odoo test exercised four folds with 20 training combinations each and verified the selected strategy and policy carry into separate validation and evaluation dates. Fresh installation and update both passed 25 tests. Concurrent worker recovery and journal checks reran. Populated upgrades directly from 20.0.9.1.0 and from 20.0.9.1.1 retained 1,243 and 1,245 existing XML IDs respectively, along with prior table digests.
- Edge passed 21 checks, including the actual **Check Upstox Readiness** button and its receipt output. The browser screenshots and raw log are in the evidence bundle.

## Release 20.0.9.1.3

- Fresh installation and module update passed all 25 ORM tests. The same-cutoff test verifies no early first-arrival reservation, a stronger candidate win, schedule order reversal, deadline expiry and journal invariants.
- The first independent attempt used a duplicate fixture source label. The next retry exposed a real context-scope error when the durable worker handed off to a requester who lacked its default company. Explicitly restricting the worker to the authorized job company fixed the problem. The independent PostgreSQL race then selected the stronger instrument with one reservation after retry.
- The reordered fixture initially left a gap in the previous completed session. Filling that prior session reproduced the same winner under both orders and retained the data quality veto.
- Populated upgrades from the P09.1 baseline and previous R01 release retained their XML IDs and record hashes.
- Edge passed all 23 checks. The two latest cases exercise the company provider-status view and the candidate instrument and observation workspace. Screenshots and logs are included.

## Release 20.0.9.1.4

- All 61 standalone tests passed. Numerical references verify warm-up, volatility, band width, relative volume spike threshold, weighted VWAP and causal benchmark matching. The archived eleven P09.1 stress outputs reproduced.
- Both Odoo fresh installation and module update passed 26 tests. The new fixture exercises Bhavcopy and authorized CSV comparison, raw-share attestation, possible split mismatch, no-research quarantine and an independently corroborated replacement. It retains the original observations. The first fixture run used an unsupported reviewed-calendar source and the corrected fixture used the canonical exchange source.
- Populated upgrades from 20.0.9.1.0 and 20.0.9.1.3 kept 1,243 and 1,261 XML IDs respectively, along with record-level hashes for the prior columns.
- Edge passed all 24 checks. The comparison review field required committing the input before viewing both controls. The corrected browser interaction verified their separate availability. Independent PostgreSQL contention and worker recovery also passed.

## Release 20.0.9.1.5

- All 63 standalone tests and all 26 Odoo fresh-install and update tests passed. The calibration test verifies exclusion of exit-bar and future marks, insufficient-sample handling, and a target constrained by the training cap and minimum net reward-to-risk.
- The Odoo fixture exercises four walk-forward folds and checks the trading dates used for the fit and the cap persisted in the replay specification. The snapshot evidence test verifies all 25 identifiers and distinguishes completed, unavailable and separate-workflow results.
- Edge passed 25 checks. The new browser case checks that fixture account and daily research event cards open lists with matching counts. Existing PostgreSQL contention and process interruption checks passed.
- Direct upgrades from 20.0.9.1.0, 20.0.9.1.3 and 20.0.9.1.4 retained earlier record hashes and 1,243, 1,261 and 1,280 XML IDs respectively. The final schema checks include an existing findings record. A separate PostgreSQL log path per test port resolves a parallel harness log-file lock.

## Release 20.0.9.1.6

- All 65 standalone tests passed. Each of G01–G14 was failed independently. The suite covers missing and malformed gate evidence, unapproved modes and reproducible hashes of the exact inputs. All eleven archived stress scenarios matched.
- Fresh Odoo installation and module update each passed 27 tests. The fixture verifies equivalent historical sources, both grants, approved failure categories and linked audit attempts. The expanded holdout test covers denied output and raw input across four Odoo roles, an alternate source label, a queued job and one risk-authorized evaluation.
- Edge passed 25 checks. Independent PostgreSQL contention, worker interruption and lease recovery passed after refreshing the verification session's transaction snapshot following the recovery worker's commit.
- The populated upgrade from 20.0.9.1.5 preserved 1,282 XML IDs and all compared record hashes, including the stored historical findings record.
- The direct upgrade from the archived P09.1 schema preserved 1,243 XML IDs and all compared record hashes. An earlier development database with the same version string lacked the archived `last_entry_check_id` column. The initial row comparison detected the newly added column, and the direct verification used the populated database with the archived schema.

## Release 20.0.9.1.7

- All 66 standalone tests passed, including fresh, stale, late and missing observation timing. The provider capability test removes each prerequisite independently. Negative data cases cover wrong source identity, invalid OHLC, schemas, timing and explicit unit conflicts. The archived eleven stress scenarios matched.
- Fresh installation and module update each passed 27 Odoo tests. The daily import fixture denies a wrong symbol and a wrong ISIN. The prospective fixture checks expiry, rejects a completed entry outside the plan's frozen range and verifies that reserved capital is returned.
- The first new range test copied a lineage-protected model. Creating an authored fixture through the normal import path resolved the failure. The upgrade harness now uses a unique disposable benchmark company so a populated clone can include earlier benchmark data.
- The 20.0.9.1.6 populated clone preserved 1,284 XML IDs and the compared historical record hashes. Independent PostgreSQL contention and interrupted-worker recovery passed.
- The populated upgrade from the archived P09.1 schema kept its 1,243 XML IDs and compared record hashes.
- Edge passed all 26 checks. The added chart case opens the selected snapshot, displays its frozen cutoff, toggles both moving averages, matches the independently known values and hides VWAP without a session calendar. The provider view identifies current connectivity as unverified. The first Edge attempt was still on the supplemental findings form when it looked for the snapshot's chart action. Returning to the snapshot fixed the test navigation.

[Commands, raw logs and screenshots](evidence/p06_p07_repair/INDEX.md)
