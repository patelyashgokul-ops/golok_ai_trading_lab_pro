# Provider capabilities — P06

| Source | Available here | Evidence and operating boundary |
| --- | --- | --- |
| Synthetic fixture | CSV, ZIP, OHLCV research, portfolio simulation and deterministic MCP protocol tests | Local authored observations. The import path still checks an explicit company review. |
| NSE Bhavcopy | Upload a lawfully held legacy CM file for a completed NSE session. All EQ rows are validated before acceptance. | CSV and single-member ZIP exercised with authored files. UDiFF, automated retrieval and real archive coverage remain open. [Official reports](https://www.nseindia.com/all-reports) |
| NSE MCP | Documented endpoints for Bhavcopy and cash-market information. Injected offline client tests initialization, ready notification, discovery, schema checks and a pinned synthetic tool call. | Published informational scope does not establish permission for storing research panels or tuning strategies. No production transport or real tool catalog was activated. [Official NSE MCP](https://www.nseindia.com/nse-mcp) · [MCP lifecycle](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle) |
| Yahoo Finance | Denied by local capability registry | The yfinance project identifies personal-use constraints and directs users to the provider terms. Verification did not establish the project's intended automated rights. No dependency installed. [Project documentation](https://github.com/ranaroussi/yfinance) |
| Angel One | Existing read-only adapter, explicitly authenticated local worker, historical sync and fixture path | Historical storage now additionally requires an effective company review. Egress and account entitlement prevent a real smoke test. |
| Upstox | Reserved source identity with no enabled operation | Owner reported inactive account segments. No authenticated transport verified. |

The router matches the requested feed class, permission set and implementation ceiling. Daily data cannot satisfy an intraday or live request. Upstream identity is tracked separately from the provider label.
