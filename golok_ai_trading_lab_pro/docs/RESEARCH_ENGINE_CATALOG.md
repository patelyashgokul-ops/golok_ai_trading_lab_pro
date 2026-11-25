# Supplemental historical research

Version 1 introduced immutable supplemental records tied to the Odoo snapshot digest. A missing or changed input window blocks recalculation. Incomplete input leaves the finding unavailable. The first release covered four computations.

| Engine | Computation |
|---|---|
| RE-03 | Ordered higher highs, lower lows and net close change over six observations |
| RE-04 | Last candle body/wicks with explicit flat, doji and rejection geometry definitions |
| RE-06 | Minimum low and maximum high over 20 preceding observations, excluding the current candle |
| RE-19 | Positive, negative and flat close transitions and net return over ten transitions |

The existing three P02 outputs remain. Findings are descriptive and snapshot-bound. They establish neither market-wide regimes nor predictive performance.

Release 20.0.9.1.5 preserves historical findings and adds a versioned evidence envelope for RE-01–RE-25. The current supplemental computations comprise ten capabilities. RE-15 counts realized up, flat and down moves in non-overlapping historical samples following a matching three-move pattern. The inventory separates the 13 implemented snapshot paths, five specialized strategy and portfolio paths and seven external-input paths.
