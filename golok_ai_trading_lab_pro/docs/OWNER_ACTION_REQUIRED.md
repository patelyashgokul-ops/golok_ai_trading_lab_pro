# Owner actions for P04

You can run synthetic session synchronization, historical snapshots, the scanner, and the synthetic replay ledger immediately. Real broker access remains disabled unless you opt in on the Odoo host. Keep credentials and account identifiers out of browser forms, terminal transcripts, screenshots, and any material sent for review.

## Confirm eligibility with Angel One

Confirm that your account permits read-only historical market data and storing it for internal research, that the Odoo host uses the provider-approved registered public egress, and that your application may retrieve the relevant exchange and symbol. Confirm applicable fees and quotas and that the candle timestamp is the opening timestamp for the requested instrument and interval. This confirmation is required before using the real synchronization mode. The documentation example includes an offset-aware candle timestamp, but the example alone does not establish the opening-time contract. [Historical and quote response contract](https://smartapi.angelone.in/docs/ResponseStructure) · [Official SDK](https://github.com/angel-one/smartapi-python) · [Registered egress guidance](https://smartapi.angelone.in/smartapi/forum/topic/5671/asking-for-static-ip-for-getting-api-for-historical-data/12)

## Configure a local session

In a private Windows PowerShell window, use masked input for credentials and start Odoo from the same shell using your established local configuration. Use a fresh TOTP code immediately before you test. Do not store the TOTP in a persistent user or machine environment. A broker token is kept in memory for up to five minutes per Odoo process and discarded on expiry or authentication failure. Generate a fresh code before restarting for reauthentication.

```powershell
$env:GOLOK_SMARTAPI_KEY = Read-Host 'Read-only app key' -MaskInput
$env:GOLOK_SMARTAPI_CLIENT_CODE = Read-Host 'Angel One client code' -MaskInput
$env:GOLOK_SMARTAPI_PIN = Read-Host 'Angel One PIN' -MaskInput
$env:GOLOK_SMARTAPI_TOTP_CODE = Read-Host 'Current TOTP code' -MaskInput
$env:GOLOK_SMARTAPI_PUBLIC_IP = Read-Host 'Registered public IPv4' -MaskInput
$env:GOLOK_SMARTAPI_LOCAL_IP = Read-Host 'Host local IPv4' -MaskInput
$env:GOLOK_SMARTAPI_MAC = Read-Host 'Host MAC address' -MaskInput
$env:GOLOK_SMARTAPI_AUTHORIZED = '1'
$env:GOLOK_SMARTAPI_HISTORY_OPEN_STAMPED = '1'
```

Set the last value only after confirming that candles are open-stamped. Shut down the broker-enabled Odoo process and close the private shell when the authorization test is complete.

## Test a single closed historical session

Create an administrator-reviewed SmartAPI mapping and operator-reviewed exchange calendar for one closed cash-equity session. Use **Synchronize Historical** → **Authorized SmartAPI historical**, select the mapping, calendar, date and interval and submit once. In **Sync History** check the attempt state, complete candle count and first and last close. A successful request can support descriptive research after its recorded receipt. Historical vendor publication time is unknown, so the result cannot be used as an as-of trading simulation or live observation.

Share only the sanitized status, interval, exchange, requested session date, candle count and returned coverage. A configuration check or login alone does not verify historical access. The app still requires separate live quote, streaming and licensed historical financial validation. A verified fee schedule and explicitly authorized point-in-time market dataset are needed before those financial tests.
