# Indicator formulas, series version 1

VWAP in this implementation is an OHLCV approximation. It does not have venue tick data, and returns unavailable after an interruption when continuity cannot be established by the indicator.

Inputs are ascending validated OHLCV. Output lists align with each observation. Warm-up and unresolved inputs return null. Calculations use Decimal with 28-digit context. The service processes up to 4,000 rows and ORM snapshots up to 250. Windows count observed bars and do not synthesize missing data. A calendar gap suppresses ORM indicator findings.

| Indicator | Formula and warm-up |
|---|---|
| SMA20, EMA20 | Mean of 20 closes. EMA seeds at the SMA, then applies alpha 2/21. |
| RSI14 | Wilder smoothing of 14 positive and negative changes. 100 × gain / (gain + loss). Both zero returns 50. |
| MACD | EMA12 − EMA26 with 9-value EMA signal and line-minus-signal histogram. Each EMA seeds from its own SMA. |
| ATR14 | Wilder smoothing of true range over 14 transitions. True range is max of high−low and absolute previous close gaps. |
| VWAP | Cumulative typical price times volume divided by total volume. Requires a calendar and uninterrupted observations from session open. Resets at each session. |
| ADX14 | Wilder-smoothed directional movements, then 14-period Wilder smoothing of their normalized absolute difference. First result after 27 transitions. |
| Bollinger20 | SMA20 ± two population standard deviations. |
| Stochastic14 | 100 × (close − lowest low) / (highest high − lowest low); null on zero range. |
| Relative volume20 | Current volume divided by preceding 20-bar mean. Null for zero mean. |
| ROC10 | Close divided by close 10 bars ago, minus one. |
| OBV | Starts at zero. Adds volume on rising closes and subtracts it on falling closes. |
| Historical volatility20 | Population standard deviation of 20 one-bar simple returns. Unannualized. |
| Rolling high / low | Highest high and lowest low over a trailing 20-bar window, inclusive of the current completed bar. |
| Opening range15 | High/low of a contiguous session-opening window, first available at the 15-minute close. |
| Relative strength | Close / aligned benchmark close. The matching benchmark observation must have been published by the instrument observation’s availability time. |
| Opening gap | Session opening observations compare the current open to the previous observed close. Confirm coverage before interpreting an overnight gap. |
| Volume spike | True when relative volume is at least 2. |
| Trend slope20 | Ordinary least squares slope over 20 equidistant close indexes, in price units per bar. |

P01 descriptive fields remain stable. Calendar-bound P02 snapshots add version 2 metadata and additional indicator values in RE-01, RE-05 and RE-18. Only those research engines have an ORM result path.
