# Exchange calendar and data time

P03 adds an optional `segments` array, for example `[["09:15","10:13"],["11:00","15:30"]]` for a synthetic split day. The outer opening and closing must match the first and last segments. Entry and exit cutoffs must fall in a continuous window. An optional `post_close` marker describes a period excluded from the continuous grid. Intraday grids restart at segment openings and allow a truncated last bar. Split-session daily observations and split-session ST-01 execution remain unsupported.

Calendar revisions are immutable, owned by one company and scoped to NSE or BSE. Trading System Administrators can create revisions. An analyst selects a revision when registering a dataset. A reviewed revision records the operator's review date and a direct HTTPS URL on that exchange's domain. The software checks the URL domain and the schedule structure. The operator is responsible for reconciling the schedule with the official notices. A fixture revision can only be used with a synthetic dataset.

Use one row per date in the coverage period. Mark exchange holidays and weekends explicitly as closed, and list an announced special session as special. Each trading date represents one continuous segment. Split sessions, intraday halts and instrument-specific closing auctions require a separate model. A date omitted from the JSON has unknown coverage.

```json
[
  {"date":"2024-01-02","kind":"regular","pre_open":"09:00","open":"09:15","close":"15:30","entry_cutoff":"14:30","exit_cutoff":"15:25"},
  {"date":"2024-01-03","kind":"closed"}
]
```

The snippet is synthetic schema documentation. Times in schedule rows are IST. OHLCV storage uses UTC. Intraday bars run from the session opening grid, with a shorter final bar when required. Daily bars span the explicit session. Pre-open bars are excluded. Gap counts cover expected closes between the first and last observed close, including wholly missing covered trading dates in between. Leading and trailing missing bars outside that observed span are outside descriptive gap counts. ST-01 imposes a stricter complete-session grid.

Calendar-bound CSV adds `open_time,available_at` after `volume`. The operator supplies the vendor publication time separately from the close. The server enforces `open_time < close_time <= available_at <= import time` and filters by publication time at the research cutoff. `ingested_at` records local arrival. Adjustments, restatements and stale quotes require additional inputs. Historical availability remains operator-supplied evidence.

Source check on 24 November 2026 covered equity pre-open/normal timings, 2026 NSE holidays and the Muhurat exception, cash-market closing auction exceptions, and BSE continuous equity hours. Verify the segment and dated notices before creating a revision. [NSE market timings](https://betanseapi.nseindia.com/static/market-data/market-timings) · [NSE 2026 holiday circular](https://nsearchives.nseindia.com/content/circulars/CMTR71775.pdf) · [NSE closing auction](https://betanseapi.nseindia.com/static/products-services/closing-auction-session) · [BSE equity cash circular](https://www.bseindia.com/markets/MarketInfo/DownloadAttach.aspx?attachedId=8a7fec3a-95bc-4bd2-82de-76e2a84e2915&id=20250429-51)
