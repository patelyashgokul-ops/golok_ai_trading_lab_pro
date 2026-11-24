# Synthetic strategy registry

Sequential ST-01 multi-3 distinguishes unresolved and risk-suspended coverage. The prior multi-1 and multi-2 outputs remain readable. Portfolio replay freezes all strategy keys, the `portfolio-1` version and implementation hashes.

| Strategy | Required observations and hypothesis | Invalidation source |
| --- | --- | --- |
| ST-01 Opening Range Breakout | The completed opening 15-minute range, a prior close inside it and a close above the range with elevated volume | Opening range low |
| ST-02 VWAP Pullback | At least six completed session bars, bullish movement before the current bar and a recovery above the cumulative prior OHLCV-derived approximate VWAP | Lower low of the preceding and signal bars |
| ST-08 Mean Reversion | Six preceding range-bound bars followed by an excursion below the range and a bullish close back inside the lower half | Low of the excursion bar |

The portfolio uses a fixed 4R preliminary target and validates reward-to-risk after fees and sizing. An entry requires a later opening within one interval and a valid session cutoff. Gap stops use the adverse opening price. A bar reaching both stop and target is resolved stop-first. An ordinary target requires trade-through. The position must close by 12 intervals or the session exit cutoff. When more than one strategy triggers simultaneously for the same instrument, the lowest strategy ID is retained. The current strategies are available for synthetic replay. Outcome diversity, promotion governance and financial validation remain open.
