# P04 independent review findings

| Issue | Finding and cause | Status and regression | Remaining scope |
|---|---|---|---|
| BUG-P04-01 | High. The previous Odoo action only tested login and discarded the token. | Added opt-in process-local token handling and a historical request wizard in `models/sync.py`. Fixture adapter-to-ORM workflow executed. | Authorized credentials, entitlement and actual historical access remain unverified. |
| BUG-P04-02 | High. P03 only had quote receipt time. | Optional FULL parsing accepts an explicitly offset-aware feed timestamp. Tests exercise stale, future, and unknown timestamps. | The provider's documented offset-less example remains UNKNOWN pending verified timezone delivery semantics. |
| BUG-P04-03 | Scope limitation. The historical replay engine explicitly accepts synthetic records. | Provider storage stays descriptive-only. Preserved synthetic isolation and tested fixture-origin controls. | Licensed temporal data and actual historical financial eligibility. |
| BUG-P04-04 | Scope limitation. `services/experiments.py` uses a single instrument and a bounded sample. | Existing bounds and synthetic replay preserved. | Checkpointed multi-instrument replay. |
| BUG-P04-05 | High. P03 recorded but did not enforce the consecutive loss count. | Multi-2 stops after two realized net losses. Three-session losing fixture rejects subsequent execution. | Portfolio-wide risk, daily loss policy and authorized administrative resume. |
| BUG-P04-06 | High. Posting previously sized fills did not require matching starting cash. | Exact paise comparison under account lock. Odoo mismatch test and independent successful same-capital replay regression. | Risk-aware account rebasing would be a separate new experiment. |
| BUG-P04-07 | Scope limitation. Replay transition accounting is virtual and bounded; portfolio risk service absent. | Existing sizing veto and reserve balance preserved. | Exposure and daily portfolio limits. |
| BUG-P04-08 | Scope limitation. Transactional queue has no durable lease state. | Existing bounded worker exercised in P04 ORM. | Separate lease, retries, cancellation after claim, and restart verification. |
| BUG-P04-09 | Medium. Traceability rows use earlier descriptions or scopes. | Updated affected acceptance and invariant rows and preserved the P03 matrix. | Full systematic reconciliation and prior scope verification remain open. |
| BUG-P04-10 | Scope limitation. Temporal labels do not isolate holdout. | Confirmed by inspecting experiment input and persistence. | Sealed consumption audit and walk-forward. |
| BUG-P04-11 | Scope limitation. Historical NO TRADE guards are distributed. | Provider origin cannot enter replay; scanner continues to show NO TRADE. | Full central G01–G14 engine and ranking. |
| BUG-P04-12 | Scope limitation. Overview had no stock scanner. | Added a company-scoped historical snapshot scanner with native filtering and pagination. | A ranked live research workspace and dedicated dashboard panels. |

An intermediate fresh-install test exposed an unsupported Selection ondelete policy. The origin choice moved into the existing field definition and was reverified in the isolated release install. See [initial install evidence](evidence/p04/runtime/installation/fresh.log) and [release tests](evidence/p04/release/installation/fresh.log).
