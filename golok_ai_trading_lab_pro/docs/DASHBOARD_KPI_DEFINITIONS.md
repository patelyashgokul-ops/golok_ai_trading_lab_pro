# Research Overview KPI definitions

The P03 cards count persisted synthetic experiments and virtual historical replay accounts in the active company. Drill-downs apply the same company scope. A zero count is the actual persisted count. It does not display implied cash or prospective performance.

All counters use the active company and native Odoo model access. Active instruments are non-archived instrument rows. Historical datasets are dataset rows across both origin types. Stored candles are immutable imported observations, including quarantined datasets. Research snapshots are persisted descriptive runs. Quarantined datasets count the rows explicitly flagged by an administrator. Latest recorded ingestion is the greatest local ingestion timestamp in the active company and is not a market freshness indicator.

The initial chart reads up to 60 bars after rechecking the snapshot hash against the original input window and filters out observations not published by the cutoff in a calendar-bound run. A backfill that changes the underlying window invalidates chart display for the older snapshot. The chart displays OHLC and relative volume bar heights from the same bounded source, with an origin label. Provider mode is offline here. This frontend does not query Angel One.

Release 20.0.9.1.5 uses a single server-side domain map for counts and list drill-downs. Quarantined datasets include administrative quarantine and material source conflicts, counted once per dataset. Prospective fixture accounts, fixture candidate records, synthetic performance reports and daily research events are persisted, active-company records. The KPI counts include only records visible to the current role.
