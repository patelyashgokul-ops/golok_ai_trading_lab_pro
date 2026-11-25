# Upstox Analytics configuration

Open **Trading Lab → Market Data API Configuration** as a Trading System Administrator in the target company. The provider starts **Offline**. An active token does not grant data-use rights.

1. Record permitted operations under **Market Data Authorization**. Keep query, display, storage, automation and descriptive research separate. Record explicit live-data permission before requesting a quote or starting a stream.
2. Create or select a reviewed NSE cash-equity mapping and a reviewed calendar for the desired dates. Select **Upstox Analytics** and **Apply Settings**. The mapping scopes the connectivity test and subscription to that security.
3. Select **Set or Replace Analytics Token**. Enter the complete token in the masked form and enter the expiry displayed by Upstox with its timezone. Save locally or through HTTPS. The save runs a policy-gated connection check. With **Offline** selected, the token can be staged without contacting the provider.
4. Use **Test Connection** to retry. An authorized REST LTP response verifies access and instrument identity. It has no exchange event timestamp. Without a live grant, an authorized historical probe can validate the complete timestamp grid for the latest matching closed 5-minute session in the reviewed calendar without storing the response.
5. **Synchronize Instrument Reference** saves the validated NSE cash-equity catalog for the active company and compares the selected ISIN, symbol and lot. Open **Instrument Catalog** to search the latest authorized revision by symbol or ISIN. Identical content is reused within the same authorization. Changed content creates a new snapshot. Existing effective-dated mappings remain authoritative. The catalog is for internal display under a current source review.
6. For automatic historical backfill, create a bounded **Historical Sync Plan** for that mapping and calendar. Enable **Automatically advance permitted historical plans**. Optionally enable **Queue descriptive research after backfill** when permitted.
7. To sample the V3 stream, enable **Collect timestamped V3 samples**. Collection reconnects on a later scheduler run after a transient failure. It accepts live LTPC updates only in a reviewed normal-open NSE equity session and checks trade, publication and receipt timestamps. Stale samples and samples without current rights are hidden.
8. To pause acquisition select **Offline** and apply. Replace the token from the masked form to rotate it. Rotation clears earlier connection and quote evidence. Use Upstox Developer Apps to revoke the token at its source.

## Credential handling

The Odoo worker encrypts the token with Windows DPAPI in current-user mode. The envelope is bound to the database and company. The private model has no generic ORM grants. Submission uses an administrator- and company-checked, CSRF-protected HTTP route. Responses contain status and expiry only. Run Odoo under a stable Windows user with its profile loaded. A renamed or copied database or a different worker account requires re-entering the token. The original environment-variable historical configuration is used when the company has no UI configuration.

## Verification scope

| Operation | Technical status |
|---|---|
| Masked entry, encrypted replacement, expiry and local role checks | Implemented for the Windows Odoo host. |
| REST LTP, single-session history, bulk NSE cash-equity catalog and bounded WebSocket LTPC sampling | Read-only adapters and fixture coverage. The catalog keeps versioned snapshots and preserves reviewed mappings. |
| Automatic permitted sync and descriptive research | Uses existing authorized history checkpoints and job queue. |
| Continuous intraday collection | The worker takes bounded samples of one configured security. Continuous complete market data collection remains open. |
| Strategy replay and prospective paper | Earlier point-in-time replay and fixture paper workflows remain available. Receipt-time history does not establish historical publication. LTPC lacks complete executable OHLCV. Direct Upstox promotion into these workflows remains incomplete. |
| Genuine account access, historical coverage, timestamp semantics and prospective financial evidence | Blocked pending entitlement and genuine validation. |

The stream uses the websocket-client package already present on the tested Windows host. Missing transport support disables stream collection. [Analytics Token](https://upstox.com/developer/api-documentation/analytics-token/) · [LTP V3](https://upstox.com/developer/api-documentation/ltp-v3/) · [Market Data Feed V3](https://upstox.com/developer/api-documentation/v3/get-market-data-feed/) · [Instruments](https://upstox.com/developer/api-documentation/instruments/)
