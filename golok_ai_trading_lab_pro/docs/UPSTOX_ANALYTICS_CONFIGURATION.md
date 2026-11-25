# Upstox Analytics configuration

Open **Trading Lab → Market Data API Configuration** as a Trading System Administrator in the target company. The provider starts **Offline**. An active token does not grant data-use rights.

1. Record permitted operations under **Market Data Authorization**. Keep query, display, storage, automation and descriptive research separate. Record explicit live-data permission before requesting a quote or starting a stream.
2. Create or select a reviewed NSE cash-equity mapping and a reviewed calendar for the desired dates. Select **Upstox Analytics** and **Apply Settings**. The mapping scopes the connectivity test and subscription to that security.
3. Select **Set or Replace Analytics Token**. Enter the complete token in the masked form and enter the expiry displayed by Upstox with its timezone. Save locally or through HTTPS. The save runs a policy-gated connection check. With **Offline** selected, the token can be staged without contacting the provider.
4. Use **Test Connection** to retry. An authorized REST LTP response verifies access and instrument identity. It has no exchange event timestamp. Without a live grant, an authorized historical probe can validate the complete timestamp grid for the latest matching closed 5-minute session in the reviewed calendar without storing the response.
5. **Synchronize Instrument Reference** saves the validated NSE cash-equity catalog for the active company and compares the selected ISIN, symbol and lot. Open **Instrument Catalog** to search the latest authorized revision by symbol or ISIN. Identical content is reused within the same authorization. Changed content creates a new snapshot. Existing effective-dated mappings remain authoritative. The catalog is for internal display under a current source review.
6. For automatic historical backfill, create a bounded **Historical Sync Plan** for that mapping and calendar. Enable **Automatically advance permitted historical plans**. Optionally enable **Queue descriptive research after backfill** when permitted.
7. To sample the V3 stream, enable **Collect timestamped V3 samples**. To keep a local connection open for repeated observations, also select **Use continuous local V3 worker** and apply. Start the worker under the same Windows identity as Odoo. Both modes accept live LTPC updates in a reviewed normal-open NSE equity session and check trade, publication and receipt timestamps. Stale samples and samples without current rights are hidden.
8. To pause acquisition select **Offline** and apply. Replace the token from the masked form to rotate it. Rotation clears earlier connection and quote evidence. Use Upstox Developer Apps to revoke the token at its source.

## Credential handling

The Odoo worker encrypts the token with Windows DPAPI in current-user mode. The envelope is bound to the database and company. The private model has no generic ORM grants. Submission uses an administrator- and company-checked, CSRF-protected HTTP route. Responses contain status and expiry only. Run Odoo under a stable Windows user with its profile loaded. A renamed or copied database or a different worker account requires re-entering the token. The original environment-variable historical configuration is used when the company has no UI configuration.

## Continuous local capture

Run the PowerShell launcher with the Odoo configuration file, database and company ID:

```powershell
./scripts/run_analytics_stream.ps1 -Config C:/path/to/odoo.conf -Database your_database -CompanyId 1
```

One worker holds an exclusive PostgreSQL session lock for the company. It takes multiple updates on each socket, renews the provider connection in bounded windows and retries transport failures through the local cooldown. Before accepting a new private observation it rechecks the configuration, current authorization, calendar and holdout scope. The worker stops accepting data when those conditions fail. Ctrl+C stops the launcher. Connection renewals and disconnects can leave gaps. The persisted LTPC observations provide price and timing evidence with no generic access or export. They do not contain independently verified complete OHLCV.

## Reviewed point-in-time archive replay

Use **Import Upstox Publication Archive** with a reviewed NSE Upstox mapping and calendar. Obtain a separately permitted archive for one completed regular session with raw share OHLCV and independently documented publication timestamps. The active Upstox source review must permit query, display, persistence and backtest and confirm raw share OHLCV.

The CSV uses the chronological header below. Time values include an explicit UTC offset and zero seconds. Availability must be the original documented publication time.

```text
close_time,open,high,low,close,volume,open_time,available_at
```

The administrator supplies the separately reviewed SHA-256 of the exact CSV bytes and the direct HTTPS evidence reference. The intake rejects a different file, incomplete session grid, out-of-order publication, an incompatible mapping or missing authorization. The accepted dataset freezes the stored candle digest and keeps the local import timestamp separately. Choose **Open Archive Replay** from the dataset, then a hypothetical tariff and strategy, and run **Authorized Historical Replay**. The archive must remain covered by its original source review. Revocation disables new replay and hides existing authorized outputs.

## Verification scope

| Operation | Technical status |
|---|---|
| Masked entry, encrypted replacement, expiry and local role checks | Implemented for the Windows Odoo host. |
| REST LTP, single-session history, bulk NSE cash-equity catalog and bounded WebSocket LTPC sampling | Read-only adapters and fixture coverage. The catalog keeps versioned snapshots and preserves reviewed mappings. |
| Automatic permitted sync and descriptive research | Uses existing authorized history checkpoints and job queue. |
| Continuous intraday collection | The optional dedicated worker accepts repeated LTPC updates for one configured security and renews bounded connections. Production-feed continuity and complete bar coverage remain unverified. |
| Historical strategy replay | Direct Upstox archive intake and authorized replay are fixture-tested. Receipt-time API history requires independent publication evidence in a separate archive before it can support this mode. |
| Prospective paper | Existing fixture-only workflows remain available. Direct Upstox prospective paper ingestion remains incomplete. LTPC samples lack complete executable OHLCV. |
| Genuine account access, historical coverage, timestamp semantics and prospective financial evidence | Blocked pending entitlement and genuine validation. |

The stream uses the websocket-client package already present on the tested Windows host. Missing transport support disables stream collection. [Analytics Token](https://upstox.com/developer/api-documentation/analytics-token/) · [LTP V3](https://upstox.com/developer/api-documentation/ltp-v3/) · [Market Data Feed V3](https://upstox.com/developer/api-documentation/v3/get-market-data-feed/) · [Instruments](https://upstox.com/developer/api-documentation/instruments/)
