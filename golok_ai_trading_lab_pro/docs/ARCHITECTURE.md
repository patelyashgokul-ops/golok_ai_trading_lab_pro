# Architecture

This add-on runs inside native Odoo 20 Community. It depends on `web` and uses the Python standard library for CSV, validation, hashing and descriptive statistics.

| Layer | Path | Behavior |
|---|---|---|
| Input contract | `services/market_data.py` | Bounded UTF-8 CSV, ordered offset-aware close timestamps, Decimal prices, OHLC invariants, integral volume, intraday gap detection |
| Descriptive analytics | `services/research.py` | SMA(20), relative volume against the prior 20 bars, Wilder ATR(14) seeded by 14 true ranges |
| Persistence | `models/lab.py` | Company-scoped instruments, immutable dataset identity, append-only candles and research snapshots |
| Import and research actions | `wizard/lab.py` | Analyst workflows for CSV import and research cutoff selection |
| Access | `security/` | Odoo 20 groups, model grants and global company filters in `ir.access.csv` |
| Interface | `views/lab.xml`, `static/src/` | Native data and research views, OWL overview and company-filtered drill-downs |

## Data flow

The dataset supplies the source label, exchange, instrument, interval and origin. An analyst uploads up to 512 KiB and 4,000 bars at a time. Each bar uses an explicit ISO 8601 close time, converted to UTC before persistence. Exact price text preserves imported Decimal precision. Stored rows capture the ingestion time and validation version. The import validates every row before creating any candles. An exact repeat reuses existing rows. A conflicting repeat raises an error before inserts. PostgreSQL enforces unique dataset and close-time pairs. A concurrent importer can receive a uniqueness error and rerun the request after the competing transaction commits.

The input contract treats dataset mapping and import rights as operator-supplied provenance. Data from different declared publishers or origins may coexist. Intraday gaps between adjacent bars on the same IST calendar date are detected in the selected research window. Exchange calendars, interval anchoring, corporate actions, incomplete provider bars and market-data entitlements require independent checks whose inputs are absent from the CSV contract.

## Research flow

The server reads at most 250 bars ordered by close time, using a ceiling at the selected cutoff, then computes on the chronological sequence. The SHA-256 fingerprint covers those exact stored bars. Dataset, cutoff, digest and engine version identify a snapshot. A matching retry returns that snapshot. A backfill can produce a different digest for the same cutoff and leaves the prior snapshot intact. The timestamp filter represents observation time. Point-in-time vendor availability and cross-instrument survivorship require additional data. An intraday gap suppresses all three findings. The bounded ATR seed begins at the start of the selected input window.

The research state currently consists of `NO TRADE` and an explicit reason. The overview reads four counts for the active company and its most recently created research snapshot. Counts use stored company-scoped rows. Active instruments exclude archived instruments. Historical and synthetic provenance labels remain visible. The dashboard renders candle close timestamps in Asia/Kolkata. Real-time freshness, recommendation expiry, strategies, backtesting and paper execution have no runtime paths in this milestone.

## Access boundaries

Viewer can read. Analyst can create datasets, use input wizards and create server-computed snapshots. System Administrator adds instrument registration and archival. Risk Manager inherits analyst access and has no separate configuration surface yet. The import checks dataset write access, validates the upload and invokes a private insert path that elevates only the candle create operation with a clean context. User-facing records have no delete grant. A deployment PostgreSQL administrator remains capable of changing the underlying database and is outside the application trust boundary.

## P02 extensions

An immutable company/exchange calendar revision links to a dataset. For these datasets, temporal bars record both boundaries and operator-supplied publication time. The ORM applies that time at the cutoff and fingerprints the calendar plus temporal observations. P01 datasets continue to use the old contract. Only System Administrators may create calendar revisions or toggle dataset quarantine. A quarantined dataset blocks imports, new research and chart reads.

The chart endpoint checks read rights and the active company, recomputes its snapshot digest and supplies at most 60 bars. The Python SmartAPI client has no Odoo button, route, cron job or saved credentials. Independent simulation services apply Decimal costs and a risk veto to one complete synthetic session. A versioned reference directory resolves supplied mappings in memory. It does not populate the ORM or authorize a provider read.

## P03 extensions

Immutable effective-dated mappings add PostgreSQL exclusions, and the import path can enforce mapping validity and tick alignment. Corporate-action notices preserve source and publication metadata while historical candles stay raw. Calendar segments explicitly represent interruptions. Split-day daily data and split-day ST-01 experiments remain unsupported.

Company-scoped experiments snapshot the exact synthetic dataset, cost, risk, strategy and calendar inputs. The historical cash journal replays completed results through atomic paise reservations and fills. The background queue uses one row claim per run and processes only historical research as the requester. SmartAPI Diagnostics is opt-in, server-side, and separate from market ingestion. Supplemental research verifies the original digest before calculating four additional results.
