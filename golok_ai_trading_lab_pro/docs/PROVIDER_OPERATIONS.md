# Provider operations

The Trading System Administrator can open **SmartAPI Diagnostics**. **Check Local Configuration** sends no network requests. **Test Authorized Authentication** requires explicit opt-in and complete local configuration. For that one test, provide `GOLOK_SMARTAPI_CLIENT_CODE`, `GOLOK_SMARTAPI_PIN` and a current `GOLOK_SMARTAPI_TOTP_CODE` in the protected process environment. Existing host and application variables are listed in [SMARTAPI_SETUP.md](SMARTAPI_SETUP.md). Successful authentication discards the in-memory token. The UI never accepts or displays credentials.

A separate committed PostgreSQL reservation paces diagnostic authentication to one attempt per 60 seconds across workers in a single database. This is a local cap. No real call was performed during P03. Historical/quote REST still require independent verification and WebSocket ingestion is pending.

Angel One's official home and docs rejected the documentation fetch on 24 November 2026. The official SDK repository and provider static-IP guidance remained accessible. Confirm account-specific data storage permission, entitlement, limits and fees with the provider. [Official SDK](https://github.com/angel-one/smartapi-python) · [Registered egress guidance](https://smartapi.angelone.in/smartapi/forum/topic/5671/asking-for-static-ip-for-getting-api-for-historical-data/12)
