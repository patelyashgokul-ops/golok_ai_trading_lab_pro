# Owner actions for P05

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
