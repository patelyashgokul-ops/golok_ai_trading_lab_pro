# Owner quick start

1. Assign a Trading Lab role in Odoo. A System Administrator registers instruments, calendar revisions, mappings and corporate notices. An Analyst imports and researches. A Risk Manager can enter hypothetical costs and post virtual replays.
2. Open **Instrument Mappings** and record an effective interval, provider token, tick size and source revision. A mapping's end date is exclusive. Give each incompatible dataset revision a distinct source label.
3. Select a calendar and, optionally, a mapping on the new **Datasets** record. Use the temporal CSV format from [EXCHANGE_CALENDAR.md](EXCHANGE_CALENDAR.md). Import only data you are allowed to use. Select synthetic origin for fabricated fixtures.
4. Run research from **Run Research** and open **Run Supplemental Findings** for validated price structure, candle geometry, rolling levels and momentum. The overview provides company counters and snapshot OHLC/volume.
5. To replay a fixture, create **Hypothetical Tariffs**, using the `tariffs` array in `tests/fixtures/p02/spec.json` as an example. Choose the synthetic dataset and date range from **Run Experiment**. Read the result and frozen specification in **Experiments**.
6. To reconcile a completed synthetic replay, create a **Virtual Account**, then open **Post Replay**. Inspect consecutive reservations and closes in **Replay Journal**. Values labeled paise are minor INR units.
7. The **Research Queue** accepts manually selected historical cutoffs. An Odoo administrator can enable the inactive scheduled action to process one queued request per minute on a running server. The queue sends no broker requests.
8. Use **SmartAPI Diagnostics** only after confirming local authorization. Never paste broker credentials into the workspace or into ChatGPT. See [PROVIDER_OPERATIONS.md](PROVIDER_OPERATIONS.md).
