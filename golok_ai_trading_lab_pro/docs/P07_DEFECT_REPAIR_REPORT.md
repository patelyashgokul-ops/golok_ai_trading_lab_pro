# P07 defect repair

| ID | Severity | Root cause in P06 | P07 evidence and remaining scope |
| --- | --- | --- | --- |
| P07-F01 | High | Portfolio selected 4R unconditionally | The default is completed resistance in services/targets.py. The explicit benchmark remains available. Causality and no-target veto are unit tested. |
| P07-F02 | High | Portfolio stopped at first sorted strategy match | services/portfolio.py evaluates all same-time candidates and ranks before shared capital allocation. Reordered instruments and strategies yield identical results. |
| P07-F03 | High | Gate inputs defaulted to literal successes | Structured simulation observations in services/decision.py and services/portfolio.py. Financial and live blocks are explicit. Complete external attestations remain open. |
| P07-F04 | High | Generic CSV only checked declared origin | models/lab.py now requires an effective company review for imported observations. See the ORM denied, accepted and expired cases. Authorization is provider-class scoped. |
| P07-F05 | High | Holdout reservation guards replay routes only | Inherited single-consumption and concurrent guard tested. Raw access and external analysis isolation remain open. |
| P07-F06 | Medium | Few bounded rolling chronological folds | P06 walk-forward regression remains available. Expanded lineage and fold policies remain open. |
| P07-F07 | High | No verified acquisition entitlement | Zero genuine sessions acquired. The provider evaluation records precise scope. |
| P07-F08 | High | Legacy-only Bhavcopy reader | services/bhavcopy.py validates the targeted UDiFF cash profile using synthetic fixtures. Authorized exchange-file comparison remains open. |
| P07-F09 | High | Cross-source logic lacks ingestion integration | Existing comparator regression retained. Automatic source conflict quarantine remains open. |
| P07-F10 | Medium | No exchange-phase scheduler | Existing manual and queued workflows retained. New orchestration open. |
| P07-F11 | Medium | No controlled restart proof | Independent contention ran. Forced restart and interruption recovery remain unverified. |
| P07-F12 | High | Rights model has no lifecycle purge | Latest grant and expiry block prohibited new import. Historical read/export policy and purge remain open. |
| P07-F13 | High | Historical paper ledger only | Historical accounting reran. Prospective lifecycle remains open. |
| P07-F14 | High | Hypothetical fees lack actual account reconciliation | Fee-aware target and risk model exercised. Real charges remain open. |
| P07-F15 | Medium | Native surfaces cover part of nine workspaces | Existing Edge flows exercised. The nine complete dashboards remain open. |
| P07-F16 | Medium | Prior statuses had dated and differing scopes | Original IDs remain intact and new evidence is scoped in P07. Full historic row-by-row reclassification remains open. |
| P07-F17 | High | Replay permits synthetic provenance only | Guard remains active. Authorized replay requires an approved panel and publication timing. |
| P07-F18 | High | No real historical or prospective sample | Real-world calibration and financial conclusions remain unavailable. |

The baseline archive records the original implementation. Junit-style unittest logs and Odoo execution evidence accompany the repairs. [P06 baseline](evidence/p07/baseline/verification.log) · [Target, ranking and UDiFF tests](../tests/unit_p07.py)
