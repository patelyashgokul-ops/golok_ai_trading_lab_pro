# Owner actions for P06P07-R01

## Upstox historical connection

The read-only adapter is implemented. The owner must confirm that the existing account can generate an Analytics Token for NSE cash-equity historical access and obtain documented permission to query, display, retain and perform internal descriptive research on the requested data. An active account segment or an approved local sample remains the external dependency. Keep any token on the local Odoo host and enter no token in the application, reports or chat.

After authorization, a Trading System Administrator records the grant in **Market Data Authorization**, creates a reviewed NSE mapping with the instrument key in the form `NSE_EQ|ISIN`, and supplies a reviewed calendar. Set `GOLOK_UPSTOX_ANALYTICS_TOKEN` through a private masked prompt and `GOLOK_UPSTOX_AUTHORIZED=1` in the local Odoo process environment. Run **Synchronize Historical** for one approved completed session. Report the date, interval, expected/actual candle count and sanitized result. The fixture mode is available without credentials.

## P09 owner action

**First route.** Ask Upstox Support to confirm historical NSE cash-equity access for the existing account. Upstox documents a free, read-only Analytics Token and historical data access without a static IP. The reported inactive-segment issue still needs an account-specific answer. Request an approved one-session export as a fallback if the current account cannot generate the token. [Analytics Token documentation](https://upstox.com/developer/api-documentation/analytics-token/) · [Upstox support](https://upstox.com/contact-us/)

### Message to Upstox Support

**Subject** — Read-only NSE cash-equity historical sample and local research permission

> I have an Upstox account and use a dynamic-IP mobile hotspot. I am testing Golok AI Trading Lab Pro on a single local workstation. Can my existing account obtain an Analytics Token for the NSE cash-equity Historical Data API if the segment is inactive? If it cannot, can you provide one completed-session cash-equity OHLCV sample through an approved download or export?
>
> Please confirm whether I may retain the sample in a private local database and use it for internal descriptive research. In a separate answer, please specify whether a longer intraday sample may be retained and used for offline backtesting and virtual paper trading. Please include the applicable retention terms, any fee, and the documentation for candle timestamps and publication delays. The proposed workflow will keep the raw data private and has no broker order execution.

**Fallback route.** Request a bounded NSE Capital Market sample directly from NSE Data & Analytics at `marketdata@nse.co.in`. Request one completed-session UDiFF/Bhavcopy CSV or ZIP, ask whether they can provide it at no charge, and ask for the permitted use and storage terms in writing. For study beyond the import check, ask separately about permissible historical intraday data, publication-time evidence and backtesting. [NSE official contact](https://www.nseindia.com/static/contact/corporate-office) · [NSE historical-data policy](https://www.nseindia.in/static/market-data/nse-data-policy)

### Use the provider's answer

- **P09-AC-042** needs one approved completed session plus local retention and descriptive research permission. Import an NSE Cash UDiFF/Bhavcopy sample through **End-of-day File Imports**, then normalize to an effective mapped daily dataset. Record sanitized row totals, session date and research result in the review evidence. A provider-specific historical CSV requires the published schema and timestamp semantics for the existing authorized CSV route.
- **P09-AC-043** needs a separate permitted intraday sample with genuine out-of-sample coverage, documented publication timing, applicable costs and validation evidence. One end-of-day file closes only the import check. Access to an API, permission to store data and permission to run backtests or prospective simulation are separate parts of the grant.
- Keep credentials and raw data local. The handoff should contain the sanitized entitlement and verification outcome.

FYERS documents a no-static-IP non-trading app, but its current API terms explicitly restrict using exchange data for paper trading and other technical tools. Do not select it for this workflow without provider clarification of the actual permitted scope. [FYERS API terms](https://fyers.in/terms-and-conditions-api) · [Provider decision matrix](FREE_MARKET_DATA_PROVIDER_EVALUATION.md)

Offline research needs no external subscription. In **Research Schedules**, select a fixture-calendar dataset, pause it or check its phase. **Daily Research Operations** displays the saved event. Local scheduling requires the laptop and Odoo to be running.

For a genuine market CSV, review the precise publisher and permit descriptive research only when the documented rights allow it. Record ongoing or fixed-term storage as specified in the grant. A transient-only authorization cannot create stored observations. Existing real datasets without bound lineage remain restricted. Start offline with the bundled synthetic fixtures. [ગુજરાતી સેટઅપ](OWNER_SETUP_GUJARATI.md)

The outstanding real-data smoke test needs one genuine file for a completed session, the actual publisher's source documentation and evidence that the applicable rights permit local archival and internal descriptive research. Use an approved local folder and record the retention terms.

To validate authorized intraday simulation with genuine data, obtain explicit backtest rights and documented per-candle publication timestamps from the publisher. Create the reviewed intraday dataset, mapping and calendar and upload the CSV in **Import historical CSV**. Open the importer again with the same complete file, enter the independently reviewed evidence URL and choose **Verify Historical Publication**. The administrator's attestation freezes the dataset. Then use **Run Authorized Historical Replay** with an explicit tariff and review **Authorized Historical Simulations**.

Use **End-of-day File Imports** for legacy NSE cash Bhavcopy or the targeted UDiFF cash profile. An authorized live feed and separately validated financial workflow remain prerequisites for future live decision support.

The optional broker setup below is needed only for an owner-authorized SmartAPI test. P06 additionally requires an effective SmartAPI source review allowing query, display and archival storage.

## Available offline

In Odoo 20 Community, a **Trading System Administrator** can create a **Historical Sync Plan** using synthetic SmartAPI-shaped rows. Select the instrument mappings, matching fixture calendars, interval and historical dates. Enter rows as a JSON object keyed by `mapping_id/YYYY-MM-DD` and save. Click **Process Next Session** to advance one task. The plan shows session status, next eligible retry time and audit reports. **Cancel Remaining** preserves completed tasks.

A **Trading Research Analyst** can use **Run Synthetic Portfolio** with distinct instruments, calendar-bound synthetic candles, one interval and a hypothetical tariff. Portfolio results show frozen input digests, virtual cash, fees, fills and decision gates. Fixtures ingested after the historical close retain their receipt timestamp and are only eligible for descriptive research. The portfolio uses purpose-built synthetic bars marked available at their modeled close.

## Access, network and timestamp checks

Confirm read-only historical market-data entitlement, the permitted exchange and symbol, applicable quotas and fees, and permission to retain that data for internal research with Angel One. Confirm that the Odoo host uses an approved egress and that timestamps on the requested candle interval are opening timestamps. The published example shows an explicit offset. Confirm opening-time semantics for your access before enabling the history flag. [SmartAPI response documentation](https://smartapi.angelone.in/docs/ResponseStructure) · [Official SDK](https://github.com/angel-one/smartapi-python) · [Registered egress guidance](https://smartapi.angelone.in/smartapi/forum/topic/5671/asking-for-static-ip-for-getting-api-for-historical-data/12)

## Authorize one local read-only test

Use a private PowerShell session on the approved Odoo host. Set the connection variables, launch a single local Odoo process from that shell and open **Provider Diagnostics**. The timestamp is the time you obtained the current code. Supply it only for the current attempt and choose **Test Authentication** promptly. A cached client belongs to that process and expires within 30 minutes or at the next midnight in Asia/Kolkata, whichever comes first. The provider can invalidate it earlier. If the code expires, restart that local process with a fresh code and choose **Test Authentication** again. The diagnostic accepts codes issued in the preceding 25 seconds.

```powershell
$env:GOLOK_SMARTAPI_KEY = Read-Host 'Read-only app key' -MaskInput
$env:GOLOK_SMARTAPI_CLIENT_CODE = Read-Host 'Angel One client code' -MaskInput
$env:GOLOK_SMARTAPI_PIN = Read-Host 'Angel One PIN' -MaskInput
$env:GOLOK_SMARTAPI_PUBLIC_IP = Read-Host 'Registered public IPv4' -MaskInput
$env:GOLOK_SMARTAPI_LOCAL_IP = Read-Host 'Host local IPv4' -MaskInput
$env:GOLOK_SMARTAPI_MAC = Read-Host 'Host MAC address' -MaskInput
$env:GOLOK_SMARTAPI_AUTHORIZED = '1'
# Enable after confirming the historical candle opening timestamp contract.
$env:GOLOK_SMARTAPI_HISTORY_OPEN_STAMPED = '1'
$env:GOLOK_SMARTAPI_TOTP_CODE = Read-Host 'Current TOTP code' -MaskInput
$env:GOLOK_SMARTAPI_TOTP_ISSUED_AT = [DateTimeOffset]::UtcNow.ToString('yyyy-MM-ddTHH:mm:sszzz')
```

Keep application credentials, client codes, PINs, OTPs and tokens on the approved host. Shut down the broker-enabled process and close the private shell after the test. The database uses a conservative local request budget per operation. Deployments sharing the same broker account need account-wide coordination before enabling concurrent clients.

## Verify one closed session

Register an administrator-reviewed SmartAPI mapping and an operator-reviewed exchange calendar. Use **Synchronize Historical** or **Historical Sync Plans**, choose the authorized mode and submit one closed session. Open **Sync History** and confirm the attempt state, expected candle count and first and last close. Share the sanitized status, exchange, interval, date and coverage counts for review. Recorded receipt supports descriptive research from that point onward.

## Evidence needed for financial research

Historical financial testing requires authorized point-in-time data, including a defensible historical publication-time contract, the exchange calendar and applicable instrument mapping. Provide permitted coverage metadata and the use authorization without attaching private account data. Applicable fee evidence includes effective-dated statutory fees, exchange charges, brokerage and the intended spread and slippage methodology. Account-specific reconciliation can use owner-approved sanitized examples. A real SmartAPI smoke test, the sealed holdout workflow and actual historical financial validation remain open.
