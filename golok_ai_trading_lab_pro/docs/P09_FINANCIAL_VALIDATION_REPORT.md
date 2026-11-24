# P09 financial metrics and validation

**Calculate Performance** freezes a versioned, company-scoped metric report derived from the existing synthetic portfolio. It reconciles gross P&L, fees, net cash and completed-trade outcomes. Expectancy includes zero-net trades and deducts costs once. Zero trades return insufficient evidence. Closed-trade drawdown uses realized trade cash. End-of-day drawdown uses flat end-of-session equity. Intraday mark-to-market drawdown, capital exposure, MAE, MFE, Sharpe, Sortino and expectancy intervals remain unavailable on the current inputs.

The historical synthetic portfolio continues to provide bounded walk-forward and single-use holdout regression. P09 does not establish persistent generalized folds and parameter-selection lineage. There are zero independently validated strategies on genuine market data. [Metrics](../services/performance.py) · [Reference cases](../tests/unit_p09.py)
