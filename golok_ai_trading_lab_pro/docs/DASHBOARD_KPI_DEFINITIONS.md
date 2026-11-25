# Research Overview KPI definitions

The P03 cards count persisted synthetic experiments and virtual historical replay accounts in the active company. Drill-downs apply the same company scope. A zero count is the actual persisted count. It does not display implied cash or prospective performance.

All counters use the active company and native Odoo model access. Active instruments are non-archived instrument rows. Historical datasets are dataset rows across both origin types. Stored candles are immutable imported observations, including quarantined datasets. Research snapshots are persisted descriptive runs. Quarantined datasets count the rows explicitly flagged by an administrator. Latest recorded ingestion is the greatest local ingestion timestamp in the active company and is not a market freshness indicator.

The initial chart reads up to 60 bars after rechecking the snapshot hash against the original input window and filters out observations not published by the cutoff in a calendar-bound run. A backfill that changes the underlying window invalidates chart display for the older snapshot. The chart displays OHLC and relative volume bar heights from the same bounded source, with an origin label. Provider mode is offline here. This frontend does not query Angel One.

Release 20.0.9.1.5 uses a single server-side domain map for counts and list drill-downs. Quarantined datasets include administrative quarantine and material source conflicts, counted once per dataset. Prospective fixture accounts, fixture candidate records, synthetic performance reports and daily research events are persisted, active-company records. The KPI counts include only records visible to the current role.

## Dashboard A–I reconciliation

| Workspace | Existing Odoo entry point | Outstanding scope |
|---|---|---|
| A. Market Command Center | Research Overview, with persisted company counts and scoped drill-downs | Independently verified market session information, benchmark coverage and market regime. |
| B. Stock Scanner | Historical Scanner, with native list search and source eligibility | Research-engine and strategy filters, momentum, relative volume and risk-decision columns. |
| C. Research Opportunities | Fixture Candidate Research, with levels, strategy trials, gate results and timing evidence | Genuine inputs and financial results. |
| D. Stock Research Detail | Open Stock Chart from the selected snapshot for bounded OHLC, volume, EMA 20, SMA 20 and eligible session VWAP at the frozen cutoff. Supplemental findings remain on the snapshot. | Instrument and date selection in one work area, plus opening-range, support, resistance and candidate-level overlays. |
| E. Paper Portfolio | Prospective Fixture Paper Accounts and Virtual Replay Accounts, with separate journals | Eligible position marks and equity and drawdown curves derived from persisted events. |
| F. Strategy Intelligence | Synthetic Strategy Performance, Walk-forward Experiments and Sealed Holdouts | Independent financial evidence and trade drill-down across the experiment views. |
| G. Risk Control Center | Fixture Risk Monitor, account form and journal. The list shows remaining risk and daily realized net with optional opening cash, reservations and position cost. Daily Research Report shows recorded risk vetoes. | Dedicated per-account rejection history and complete reconciliation across historical dates. |
| H. Provider and System Health | Provider Diagnostics, Sync History, Historical Sync Plans and comparison records | Current authenticated health, verified feed freshness and workstation telemetry. |
| I. Daily Research Report | Open a session event in Daily Research Operations to see the company and date's persisted phases, coverage, strategy trials, candidate rejection reasons, risk vetoes, broker failures and realized virtual results. | Genuine market regime and independently validated prospective results. |

The session report recomputes from records visible to the current user. It uses the largest observed coverage per schedule to avoid counting the same input twice across phases. Phase and rejection counts are exact under that scope. Strategy codes come from a bounded sample of saved candidate trials. Broker failures are failures of logged requests for the session date. The virtual result includes closed orders tied to observation-driven candidates. It displays unavailable when there are no such closed orders.
