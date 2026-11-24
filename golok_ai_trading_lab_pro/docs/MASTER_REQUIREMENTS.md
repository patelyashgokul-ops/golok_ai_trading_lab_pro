# GOLOK AI TRADING LAB PRO
## MASTER AGENTIC DEVELOPMENT PROMPT 01 — PROFESSIONAL QUANTITATIVE TRADING RESEARCH PLATFORM

### 1. YOUR ROLE

Act as a multidisciplinary senior engineering and quantitative research team consisting of:

- Principal Odoo 20 Community Architect.
- Senior Python Software Engineer.
- Quantitative Trading Researcher.
- Financial Market Data Engineer.
- Intraday Trading Strategy Researcher.
- Statistical Modeling Specialist.
- Machine Learning Engineer.
- Portfolio Risk Management Specialist.
- Angel One SmartAPI Integration Engineer.
- PostgreSQL Performance Engineer.
- Senior OWL JavaScript Developer.
- Professional Financial Dashboard UX/UI Designer.
- Cybersecurity Engineer.
- Software Quality Assurance Engineer.
- Automated Testing Engineer.
- DevOps and Release Engineering Specialist.

Apply the documented research discipline, statistical methods, capital protection principles, and engineering practices associated with experienced professional traders and institutional quantitative research teams.

Do not claim to possess actual decades of trading experience, proprietary institutional strategies, or guaranteed profitable trading capabilities.

Your responsibility is to BUILD, TEST, DEBUG, VALIDATE, and DOCUMENT a working application.

Do not merely provide architectural suggestions, sample code, pseudocode, or a development plan.

Work directly in the available development environment.

---

### 2. PROJECT IDENTITY

- Product Name: Golok AI Trading Lab Pro.
- Company: Golok Technology.
- Technical Module Name: `golok_ai_trading_lab_pro`.
- Platform: Odoo 20 Community Edition.
- Backend: Python.
- Database: PostgreSQL.
- Frontend: Native Odoo OWL, JavaScript, XML, and SCSS.
- Primary Market: Indian Equity Market.
- Primary Exchange: NSE.
- Secondary Exchange: BSE, subject to provider support.
- Primary Broker Data Provider: Angel One SmartAPI.
- Primary Trading Research Type: Intraday Equity Trading.
- Secondary Research Types: Swing and Positional Trading.
- Deployment: Localhost.
- Timezone: Asia/Kolkata.
- Currency: INR.
- Hardware: CPU-only laptop.
- Available RAM: 16 GB.
- Dedicated GPU: Not available.
- Paid AI APIs: Not available.
- Local LLMs: Not required.
- Target mandatory software subscription cost: Zero.

The product must operate without OpenAI API, Claude API, Gemini API, Ollama, DeepSeek, Qwen, or any other LLM dependency.

Lightweight CPU-based machine learning is permitted.

The word AI in the product name refers to computational intelligence, statistical research, adaptive strategy evaluation, and permitted lightweight machine learning.

---

### 3. PRIMARY BUSINESS OBJECTIVE

Build a professional-grade quantitative stock market research and trading decision-support platform that identifies evidence-supported intraday trading opportunities.

The primary objective is not to generate the maximum number of tips.

The primary objectives are:

1. Maximize sustainable risk-adjusted expected returns.
2. Identify statistically supported trading opportunities.
3. Minimize unnecessary and low-quality trades.
4. Protect trading capital.
5. Detect unfavorable market conditions.
6. Reject opportunities without sufficient evidence.
7. Account for actual trading costs.
8. Improve strategy evaluation through reproducible research.
9. Provide transparent trading recommendations.
10. Continuously measure actual strategy performance.

A day with zero trading recommendations must be considered a valid outcome.

Never guarantee profits.

Never invent a profitability percentage, win rate, market price, financial result, or statistical confidence value.

---

### 4. STRICT CURRENT DEVELOPMENT SCOPE

The current product must be a research, recommendation, monitoring, backtesting, and paper trading platform.

The application may:

- Retrieve authorized live market data.
- Retrieve historical market data.
- Research stocks.
- Generate trading recommendations.
- Suggest entry prices.
- Suggest stop-loss prices.
- Suggest target prices.
- Calculate suggested position sizes.
- Monitor active recommendations.
- Generate exit alerts.
- Simulate paper trades.
- Calculate hypothetical trading performance.

The application MUST NOT:

- Place real broker orders.
- Modify real broker orders.
- Cancel real broker orders.
- Automatically buy real shares.
- Automatically sell real shares.
- Transfer funds.
- Allocate real account capital automatically.
- Implement autonomous real-money trading.

Do not implement hidden or dormant real-order execution code.

Real-money trades will be performed manually by the owner using Angel One.

Future real-order execution is explicitly outside the current project scope.

---

### 5. MANDATORY AGENTIC DEVELOPMENT WORKFLOW

Before implementation:

1. Inspect the existing repository.
2. Locate the actual Odoo installation.
3. Identify Odoo version and edition.
4. Identify Python and PostgreSQL versions.
5. Inspect available hardware resources.
6. Detect operating system and CPU capabilities.
7. Inspect Git status.
8. Detect existing module files.
9. Preserve existing valid development.
10. Identify installed dependencies.
11. Identify available testing infrastructure.
12. Verify access to official technical documentation.

Create persistent project documentation:

- `docs/MASTER_REQUIREMENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/REQUIREMENTS_TRACEABILITY.md`
- `docs/DEVELOPMENT_PLAN.md`
- `docs/DECISION_LOG.md`
- `docs/RISK_REGISTER.md`

Maintain these documents throughout development.

Assign stable requirement identifiers to all mandatory requirements.

Implement in dependency order.

Do not create a large collection of empty models, nonfunctional menus, placeholder methods, or unfinished features and claim completion.

Prefer genuinely working vertical slices over broad superficial implementation.

If the available execution context prevents completing the entire scope, prioritize the foundational and data-integrity components, document incomplete requirements precisely, and leave the project in a stable, testable state.

---

### 6. TECHNICAL ARCHITECTURE

Design a modular architecture with clear separation between:

- Odoo business models.
- Data provider adapters.
- Instrument reference data.
- Market data ingestion.
- Historical data storage.
- Data quality validation.
- Feature engineering.
- Quantitative research.
- Strategy execution.
- Statistical validation.
- Signal generation.
- Risk management.
- Portfolio simulation.
- Backtesting.
- Paper trading.
- Notifications.
- Dashboard services.
- Background research jobs.
- Security.
- Diagnostics.
- Audit evidence.

Keep quantitative algorithms independently testable.

Avoid tightly coupling numerical calculations to the Odoo ORM.

Use versioned interfaces between the research engines and market data providers.

Recommended directory structure:

```text
golok_ai_trading_lab_pro/
    __init__.py
    __manifest__.py
    models/
    services/
        providers/
        market_data/
        data_quality/
        features/
        research/
        strategies/
        statistics/
        machine_learning/
        signals/
        risk/
        backtesting/
        paper_trading/
        notifications/
        diagnostics/
    controllers/
    security/
    views/
    wizard/
    data/
    static/
        src/
            components/
            js/
            xml/
            scss/
        description/
    tests/
    docs/
    scripts/
```

Adapt the structure to verified Odoo 20 conventions.

Do not use unsupported or obsolete APIs from earlier Odoo versions.

---

### 7. ZERO PAID AI AND LOW-RESOURCE REQUIREMENTS

Optimize the entire application for a CPU-only machine with 16 GB RAM.

Mandatory restrictions:

- No LLM runtime.
- No GPU dependency.
- No mandatory cloud computing.
- No mandatory paid AI API.
- No mandatory external paid analytics service.
- No unnecessary Redis, Kafka, Elasticsearch, or heavyweight distributed architecture.
- No unnecessary deep learning framework.
- No uncontrolled parallel execution.
- No unbounded memory consumption.

Use suitable lightweight technologies when justified:

- NumPy.
- Pandas.
- SciPy.
- Scikit-learn.
- XGBoost with controlled CPU resources.
- Python standard library.
- PostgreSQL.
- Lightweight financial NLP dictionaries.
- Native Odoo scheduled actions.

Implement:

- Bounded batch processing.
- Configurable worker limits.
- CPU thread limits.
- Memory monitoring.
- Configurable cache limits.
- Incremental indicator calculations.
- Efficient database indexes.
- Bulk ingestion.
- Historical data retention policies.
- Graceful overload handling.
- Background job recovery.
- Persistent processing checkpoints.

Research workload must never block normal Odoo dashboard interaction for prolonged periods.

Use performance measurements to establish realistic stock universe sizes and refresh intervals.

Do not claim that scanning 1,000 stocks at a particular frequency is supported until measured.

---

### 8. ANGEL ONE SMARTAPI INTEGRATION

Use Angel One SmartAPI as the primary authorized market data provider.

Official references:

- https://smartapi.angelone.in/
- https://smartapi.angelone.in/docs
- https://github.com/angel-one/smartapi-python

Verify current documentation before implementation.

Record:

- Verification date.
- Supported authentication methods.
- API pricing and access conditions.
- Static IP requirements.
- Data entitlement restrictions.
- REST API rate limits.
- WebSocket subscription limits.
- Historical data restrictions.
- Session expiration behavior.
- Supported exchanges and instrument types.

Implement, where authorized:

- Secure credential configuration.
- Session authentication.
- Session renewal or controlled reauthentication.
- Instrument master synchronization.
- Instrument token mapping.
- Historical candle retrieval.
- Live quote retrieval.
- WebSocket market data ingestion.
- Heartbeat monitoring.
- Reconnection management.
- Subscription management.
- Exponential backoff.
- Provider health monitoring.
- Rate-limit-aware request scheduling.
- Error classification.
- Connectivity diagnostics.

Do not bypass broker restrictions, authentication requirements, static IP requirements, or subscription conditions.

Do not expose secrets in frontend assets, screenshots, source control, logs, exception messages, or reports.

Use environment-based secrets or an appropriately protected local secret store.

The application must install and operate in simulation mode without real broker credentials.

If credentials are unavailable, mark real integration testing as BLOCKED. Mock or fixture testing must not be represented as successful live API verification.

---

### 9. MARKET DATA QUALITY ENGINE

This is a critical foundation.

Implement validation for:

- Duplicate candles.
- Missing candles.
- Invalid prices.
- Negative or invalid volume.
- Invalid OHLC relationships.
- Out-of-order ticks.
- Incorrect instrument mappings.
- Incorrect timestamps.
- Future-dated observations.
- Stale market data.
- Incomplete candles.
- Missing trading sessions.
- Provider disconnects.
- Corporate actions.
- Stock splits.
- Bonus issues.
- Delisted and suspended instruments.
- Exchange calendar differences.
- Trading holidays.
- Special trading sessions.

Store:

- Data source.
- Exchange.
- Instrument identifier.
- Market timestamp.
- Ingestion timestamp.
- Data interval.
- Quality status.
- Data freshness.
- Processing version.

Distinguish real, delayed, historical, imported, and synthetic fixture data.

Synthetic data must never generate a live actionable trading recommendation.

Do not silently substitute delayed data for real-time data.

Stale or invalid required data must cause actionable intraday recommendations to be blocked or invalidated.

Implement idempotent ingestion and prevent duplicate records using database-backed constraints.

Provide controlled historical import support using legally authorized datasets.

---

### 10. PROFESSIONAL RESEARCH ENGINE FRAMEWORK

Create a standardized interface for the following 25 research capabilities.

- RE-01: Technical Analysis.
- RE-02: Fundamental Analysis.
- RE-03: Price Action Analysis.
- RE-04: Candlestick Pattern Analysis.
- RE-05: Volume Intelligence.
- RE-06: Support and Resistance.
- RE-07: Breakout Detection.
- RE-08: False Breakout Detection.
- RE-09: Market Trend Analysis.
- RE-10: Sector Performance and Rotation.
- RE-11: Benchmark Index Analysis.
- RE-12: Global Market Context.
- RE-13: Financial News and Event Analysis.
- RE-14: Institutional Activity Proxies.
- RE-15: Historical Pattern Analysis.
- RE-16: Statistical Probability Estimation.
- RE-17: Liquidity Analysis.
- RE-18: Volatility Analysis.
- RE-19: Momentum Analysis.
- RE-20: Abnormal Market Activity Detection.
- RE-21: Entry Optimization.
- RE-22: Stop-Loss Optimization.
- RE-23: Profit Target Optimization.
- RE-24: Historical Strategy Performance.
- RE-25: Net Expected Profit and Risk Validation.

Each research capability must return a structured result containing:

- Engine identifier.
- Engine version.
- Instrument.
- Research timestamp.
- Required input data.
- Input data freshness.
- Observed findings.
- Supporting evidence.
- Contradictory evidence.
- Applicable strategy.
- Research score, if applicable.
- Known limitations.
- Missing data.
- Quality warnings.
- Execution duration.
- Result status.

Supported statuses must include:

- COMPLETED.
- NOT_APPLICABLE.
- INSUFFICIENT_DATA.
- STALE_DATA.
- ERROR.

Do not assign positive default scores when data is missing.

Do not pretend to know institutional order flow when only indirect proxies are available.

Do not claim market manipulation has been established solely from abnormal price or volume behavior.

Do not force every research capability to influence every intraday signal. Apply relevant engines according to strategy type and data availability.

---

### 11. TECHNICAL INDICATOR LIBRARY

Implement mathematically correct, independently tested indicators.

Required indicators include:

- SMA.
- EMA.
- RSI.
- MACD.
- ATR.
- VWAP.
- ADX.
- Bollinger Bands.
- Stochastic Oscillator.
- Relative Volume.
- Rate of Change.
- On-Balance Volume.
- Historical Volatility.
- Rolling Highs and Lows.
- Opening Range.
- Relative Strength.
- Price Gaps.
- Volume Spikes.
- Trend Slopes.

Support appropriate intervals:

- 1 minute.
- 3 minutes.
- 5 minutes.
- 15 minutes.
- 30 minutes.
- 1 hour.
- Daily.

Respect provider availability and data granularity.

VWAP must reset according to the applicable trading session.

Handle indicator warm-up requirements correctly.

Never generate misleading values from insufficient historical observations.

Prevent look-ahead bias in every indicator and feature calculation.

Validate numerical results using known reference fixtures and independent implementations where practical.

---

### 12. PROFESSIONAL TRADING STRATEGY LIBRARY

Implement a versioned and extensible strategy framework.

Initial strategy candidates:

- ST-01: Opening Range Breakout.
- ST-02: VWAP Pullback.
- ST-03: VWAP Reclaim.
- ST-04: Trend Following.
- ST-05: Momentum Continuation.
- ST-06: Volume Confirmed Breakout.
- ST-07: Support and Resistance Breakout.
- ST-08: Mean Reversion.
- ST-09: Gap Continuation.
- ST-10: Gap Reversal.
- ST-11: Multi-Timeframe Trend Confirmation.
- ST-12: Relative Strength Momentum.
- ST-13: Sector Rotation.
- ST-14: Volatility Compression Breakout.
- ST-15: Trend Pullback.
- ST-16: False Breakout Reversal.
- ST-17: Statistical Reversion.
- ST-18: ATR-Based Channel Breakout.
- ST-19: Momentum Exhaustion.
- ST-20: Market Regime Adaptive Strategy.

These are research candidates, not proven profitable strategies.

Each strategy must define:

- Applicable market conditions.
- Required data.
- Entry conditions.
- Exit conditions.
- Stop-loss methodology.
- Target methodology.
- Invalidation conditions.
- Position sizing constraints.
- Applicable timeframes.
- Supported instruments.
- Trading costs.
- Historical validation requirements.
- Strategy version.

A strategy must remain in research-only status until supported by appropriate validation.

Never enable a strategy merely because its implementation exists.

---

### 13. MARKET REGIME INTELLIGENCE

Create a market regime classification framework capable of identifying:

- Bullish trends.
- Bearish trends.
- Sideways markets.
- High-volatility markets.
- Low-volatility markets.
- Strong momentum conditions.
- Weak momentum conditions.
- Market stress.
- Abnormal market conditions.
- Insufficient evidence.

Use observable market data and transparent quantitative methods.

Strategies must be evaluated against compatible market regimes.

Avoid forcing trend-following strategies into unsuitable range-bound conditions.

Avoid treating a regime classification as a guaranteed future market direction.

Implement a configurable market-wide NO TRADE decision when market quality deteriorates.

---

### 14. MASTER DECISION ENGINE

Create a centralized decision engine responsible for:

1. Gathering applicable research results.
2. Validating data availability.
3. Checking strategy eligibility.
4. Checking strategy historical performance.
5. Evaluating liquidity.
6. Evaluating volatility.
7. Evaluating market regime.
8. Detecting contradictory evidence.
9. Calculating expected net profitability.
10. Evaluating estimated downside.
11. Checking entry quality.
12. Validating stop loss.
13. Validating target feasibility.
14. Checking risk-to-reward.
15. Checking recommendation freshness.
16. Applying hard rejection rules.
17. Ranking eligible candidates.
18. Generating explainable decisions.

Supported decision states:

- BUY.
- SELL / SHORT OPPORTUNITY.
- WATCH.
- WAIT FOR ENTRY.
- HOLD EXISTING POSITION.
- EXIT.
- NO TRADE.
- INVALIDATED.
- EXPIRED.

Short recommendations must remain disabled unless supported by applicable market rules, instrument eligibility, and validated strategy behavior.

Do not treat correlated technical indicators as independent confirmation.

Do not require arbitrary unanimous agreement across unrelated research engines.

Do not use arbitrary weighted scores as proof of probability.

Hard data-quality and risk rules must never be overridden by a high research score.

---

### 15. SIGNAL QUALITY SCORING

Implement a transparent, configurable scoring framework.

Initial research score range: 0–100.

Proposed classifications:

- A+: 95–100.
- A: 90–94.
- B: 85–89.
- Watchlist: 80–84.
- Rejected: Below 80.

These are initial candidate thresholds, not validated profitability thresholds.

Initial actionable eligibility may require a minimum score of 90, subject to independent evidence and risk validation.

Implement:

- Configurable weighting.
- Strategy-specific scoring.
- Missing-data handling.
- Negative evidence penalties.
- Score decomposition.
- Versioned score configuration.
- Historical score-performance analysis.
- Calibration analysis.
- Threshold sensitivity analysis.

Distinguish clearly between:

- Research quality score.
- Expert-system agreement.
- Historical observed win rate.
- Calibrated estimated probability.
- Expected return.
- Statistical uncertainty.

Never display a score of 95/100 as a 95% chance of profit.

---

### 16. STATISTICAL PROFIT OPTIMIZATION

The objective is positive, sustainable net trading expectancy, not maximum historical win rate.

Implement calculations for:

- Gross return.
- Net return.
- Average winning trade.
- Average losing trade.
- Win rate.
- Loss rate.
- Expected value per trade.
- Profit factor.
- Maximum drawdown.
- Risk-to-reward ratio.
- Sharpe ratio where statistically meaningful.
- Sortino ratio where statistically meaningful.
- Downside risk.
- Turnover.
- Consecutive losses.
- Maximum adverse excursion.
- Maximum favorable excursion.
- Sample size.
- Confidence intervals.
- Performance stability across market regimes.

Expected trade profitability must include estimated execution costs.

Conceptual expectancy:

```text
Net Expectancy =
    Probability of Win × Average Gross Win
    − Probability of Loss × Average Gross Loss
    − Average Trading Costs
```

Extend this methodology appropriately for neutral outcomes and variable exits.

Avoid double-counting transaction costs.

Probabilities must be based on sufficient relevant evidence.

When sample sizes are insufficient, return insufficient evidence instead of fabricated confidence.

Implement conservative uncertainty handling.

Reject strategies with weak out-of-sample evidence, unacceptable drawdowns, excessive sensitivity, or negative expected net returns.

---

### 17. TRANSACTION COST ENGINE

Build a configurable Indian equity trading cost model.

Support applicable costs:

- Brokerage.
- Securities Transaction Tax.
- Exchange transaction charges.
- SEBI charges.
- GST.
- Stamp duty.
- Bid-ask spread.
- Slippage.
- Other applicable verified costs.

All tariff configurations must include:

- Effective date.
- Instrument type.
- Transaction side.
- Source.
- Verification status.

Do not hardcode unverified current statutory charges.

If actual cost settings have not been verified, clearly label the output as an estimate.

Do not calculate misleading net profit by ignoring material execution costs.

---

### 18. ADVANCED CAPITAL PROTECTION ENGINE

Implement independently enforceable risk rules.

Initial configurable conservative defaults:

- Maximum planned risk per trade: 0.5% of configured capital.
- Maximum planned daily loss threshold: 1%.
- Maximum daily paper-trade entries: 3.
- Consecutive loss pause threshold: 2.
- Minimum planned risk-to-reward: 1:2.
- Preferred candidate risk-to-reward: 1:3.
- Leverage: Disabled.
- Averaging losing positions: Disabled.
- Martingale strategies: Prohibited.
- Unlimited position sizing: Prohibited.
- Overnight intraday positions: Prohibited in simulation policy.

Implement:

- Risk-based position sizing.
- Capital-based position limits.
- Liquidity constraints.
- Stop-loss distance validation.
- Tick-size validation.
- Volatility-based risk adjustment.
- Portfolio exposure tracking.
- Correlation risk.
- Sector concentration limits.
- Market-wide risk filters.
- Daily loss monitoring.
- Consecutive loss detection.
- Strategy suspension.
- Research suspension.
- Paper trading kill switch.

Use explicit reference capital for suggested position sizing.

Example:

```text
Quantity = Minimum of:
    Quantity allowed by capital limit
    Quantity allowed by risk budget
    Quantity allowed by liquidity limits
```

Account for estimated fees and adverse execution where appropriate.

Risk limits are planned controls, not guarantees of maximum actual loss.

No automatic allocation or execution involving real account funds is permitted.

---

### 19. HISTORICAL BACKTESTING ENGINE

Build a reproducible, event-aware backtesting framework.

Mandatory requirements:

- Chronological data processing.
- No future data leakage.
- No look-ahead bias.
- Survivorship bias controls.
- Corporate action handling.
- Realistic entry timing.
- Realistic exit timing.
- Bid-ask spread modeling.
- Transaction cost modeling.
- Slippage modeling.
- Liquidity constraints.
- Stop-loss execution assumptions.
- Market session boundaries.
- Trading holiday handling.
- Partial fill modeling where supported.
- Reproducible strategy parameters.

Do not assume entry at a candle price that was unavailable when the decision was made.

If both target and stop loss are crossed inside the same candle and execution order cannot be determined, apply a documented conservative ambiguity policy or use finer-grained data.

Do not automatically assume the profitable outcome.

Implement:

- In-sample training.
- Out-of-sample evaluation.
- Walk-forward testing.
- Time-series cross-validation.
- Parameter sensitivity analysis.
- Stress testing.
- Monte Carlo or appropriate block-bootstrap analysis.
- Benchmark comparison.
- Reproducible experiment identifiers.

Do not optimize strategy parameters against the final holdout dataset.

Do not report simulated returns as actual realized returns.

---

### 20. LIGHTWEIGHT MACHINE LEARNING

Machine learning is optional per strategy and mandatory only when justified by evidence.

Permitted approaches:

- Logistic regression.
- Random forest with controlled depth.
- Gradient boosting.
- CPU-optimized XGBoost.
- Lightweight regime classification.
- Statistical probability calibration.

Implement:

- Time-aware train/test separation.
- Feature versioning.
- Model versioning.
- Reproducible random seeds.
- Training data provenance.
- Leakage detection.
- Class imbalance analysis.
- Probability calibration.
- Model drift monitoring.
- Model performance tracking.
- Safe model rollback.

Avoid uncontrolled hyperparameter search.

Compare machine learning against simpler statistical and rule-based baselines.

Reject complex models that fail to demonstrate meaningful improvement.

Never automatically promote an experimental model into actionable signal generation.

---

### 21. AUTOMATIC PAPER TRADING

Create a realistic paper trading environment.

Default configurable virtual capital: INR 50,000.

Required functionality:

- Virtual trading accounts.
- Opening balance.
- Available virtual cash.
- Reserved cash.
- Simulated orders.
- Simulated executions.
- Open positions.
- Closed positions.
- Simulated stop-loss exits.
- Simulated profit targets.
- Partial profit booking.
- Trailing stop logic.
- Intraday square-off.
- Realistic transaction costs.
- Daily realized P&L.
- Unrealized P&L.
- Net virtual equity.
- Drawdown tracking.
- Trading journal.

Paper trading may use validated market data automatically.

All balances and transactions must be explicitly identified as virtual.

Use consistent, auditable accounting rules for virtual cash and positions.

Prevent duplicate executions.

Ensure atomic state transitions.

Handle crashes, restarts, stale feeds, gaps, and unavailable market data.

Never connect paper-trading execution to real broker order APIs.

---

### 22. PROFESSIONAL TRADING RECOMMENDATION FORMAT

Every actionable recommendation must contain:

- Unique Signal ID.
- Instrument name and symbol.
- Exchange.
- Strategy name and version.
- Trading type.
- BUY or permitted SELL direction.
- Generation time in IST.
- Validity expiry.
- Latest verified price.
- Price observation timestamp.
- Entry range.
- Stop-loss price.
- Target 1.
- Target 2, if justified.
- Target 3, if justified.
- Suggested quantity.
- Required capital.
- Estimated gross profit.
- Estimated net profit.
- Estimated planned loss.
- Trading cost assumptions.
- Planned risk-to-reward.
- Research quality score.
- Supporting evidence.
- Contradictory evidence.
- Historical performance reference.
- Sample size.
- Relevant market conditions.
- Risk warnings.
- Data quality status.
- Signal invalidation conditions.

Do not invent multiple targets solely to populate the UI.

Do not generate a precise estimated win probability without sufficient statistical calibration.

Provide an explanation of why the trade qualifies.

Provide an explanation of why rejected candidates failed.

---

### 23. INTRADAY SIGNAL MONITORING

Continue monitoring recommendations after generation.

Detect:

- Entry zone reached.
- Entry no longer valid.
- Excessive price movement.
- Target reached.
- Stop-loss threshold reached.
- Trailing stop update.
- Market reversal.
- Liquidity deterioration.
- Market data disconnect.
- Signal expiry.
- Intraday session closing.
- Strategy invalidation.

Generate alerts for:

- New qualified opportunity.
- Wait for entry.
- Entry opportunity available.
- Target observation.
- Stop-loss warning.
- Exit suggestion.
- Recommendation invalidated.
- Emergency market warning.
- NO TRADE condition.

An observed price crossing must not be represented as proof that the user executed a real trade.

Support optional manual recording of actual user trades, clearly separated from paper-trade records.

Do not expose real-order execution functionality.

---

### 24. PREMIUM NATIVE ODOO TRADING DASHBOARD

This is a mandatory high-priority product requirement.

Build an elegant, professional financial trading research interface under the Golok Technology brand.

The dashboard must be functional and backed by verified database records.

Do not build a static HTML mockup and claim that the dashboard is completed.

Use native Odoo 20 Community-compatible OWL components.

Design a modern financial analytics interface with:

- Excellent information hierarchy.
- Professional typography.
- Consistent spacing.
- Clean financial charts.
- Meaningful status colors.
- Responsive layout.
- Light and dark theme compatibility where supported.
- Accessible controls.
- Loading states.
- Empty states.
- Error states.
- Stale-data warnings.
- Clear timestamps.
- Smooth, bounded refresh behavior.

Avoid unnecessary animation, oversized graphics, heavy frontend frameworks, and unnecessary CDN dependencies.

#### Dashboard A: Market Overview

Display:

- Nifty 50.
- Bank Nifty.
- Other available authorized benchmark indices.
- Market status.
- Market breadth.
- Advancing and declining instruments.
- Market regime.
- Volatility status.
- Sector performance.
- Market data freshness.

#### Dashboard B: Professional Research Scanner

Display:

- Total eligible instruments.
- Instruments scanned.
- Instruments awaiting research.
- Instruments rejected.
- Qualified candidates.
- Active strategies.
- Research execution status.
- Data quality failures.
- Research duration.

Include filterable, sortable instrument tables.

#### Dashboard C: Best Trading Opportunities

Display:

- Ranked trading opportunities.
- Signal direction.
- Research score.
- Entry range.
- Stop loss.
- Profit targets.
- Estimated net return.
- Planned risk.
- Risk-to-reward.
- Validity.
- Research evidence.

Clearly highlight whether a signal is actionable, experimental, expired, invalidated, or based on delayed data.

#### Dashboard D: Stock Research Terminal

Provide detailed instrument research:

- Candlestick chart.
- Volume chart.
- Relevant technical indicator overlays.
- Support and resistance levels.
- Strategy analysis.
- Entry and exit levels.
- Multi-timeframe research.
- Applicable research engine results.
- Positive and negative evidence.
- Data quality status.

Use efficiently aggregated and bounded chart data.

#### Dashboard E: Paper Trading Portfolio

Display:

- Initial virtual capital.
- Available virtual capital.
- Current equity.
- Open virtual positions.
- Closed virtual positions.
- Realized virtual P&L.
- Unrealized virtual P&L.
- Net virtual return.
- Equity curve.
- Drawdown curve.
- Daily performance.
- Trading journal.

#### Dashboard F: Strategy Intelligence

Display:

- Strategy performance ranking.
- Historical win rates.
- Net expectancy.
- Sample sizes.
- Maximum drawdowns.
- Profit factor.
- Market regime performance.
- Out-of-sample results.
- Validation status.
- Active and suspended strategies.

#### Dashboard G: Risk Control Center

Display:

- Configured risk limits.
- Current paper portfolio exposure.
- Daily loss threshold.
- Consecutive losses.
- Sector concentration.
- Risk rejection reasons.
- Market-wide warnings.
- Paper trading suspension state.

#### Dashboard H: Research and System Health

Display:

- Angel One connectivity.
- Market data provider status.
- Session status.
- WebSocket status.
- Last successful data update.
- Data lag.
- Background job queue.
- CPU utilization.
- Memory utilization.
- Storage usage.
- Research errors.
- Last completed research cycle.

#### Dashboard I: Daily Research Report

Display:

- Market summary.
- Qualified opportunities.
- Rejected opportunities.
- Rejection reasons.
- Most relevant research findings.
- Paper trading performance.
- Strategy warnings.
- Data limitations.
- Market risk conditions.

All KPI values must have documented and testable calculation definitions.

Every drill-down must apply correct access controls and filters.

Never show fake live prices or fictional performance as genuine.

---

### 25. AUTOMATED RESEARCH SCHEDULING

Implement timezone-aware research scheduling.

Support:

- Pre-market research.
- Market opening analysis.
- Intraday research cycles.
- Signal monitoring.
- Market closing research.
- Daily paper trading reports.
- Historical data synchronization.
- Data quality maintenance.
- Strategy performance review.

Use verified exchange trading sessions.

Respect weekends, holidays, and special sessions.

Implement:

- Persistent job status.
- Job locking.
- Retry policies.
- Duplicate-job protection.
- Timeout handling.
- Failure recovery.
- Scheduler monitoring.
- Missed-job handling.

Prevent overlapping research jobs from corrupting data or exhausting CPU resources.

Do not assume localhost jobs run when the laptop is powered off or asleep.

---

### 26. CONTINUOUS STRATEGY IMPROVEMENT

Track strategy and research engine performance over time.

Implement a controlled research feedback loop:

1. Record original recommendations.
2. Preserve the original research inputs.
3. Preserve original strategy and configuration versions.
4. Record subsequent observable outcomes.
5. Evaluate successful and unsuccessful recommendations.
6. Analyze performance by market regime.
7. Analyze score quality.
8. Identify statistically meaningful improvements.
9. Create experimental strategy versions.
10. Validate experimental versions independently.
11. Compare against the existing baseline.
12. Require explicit approval before promotion.

Never rewrite historical recommendations to make performance appear better.

Never silently change the original entry, stop loss, or target after observing the outcome.

Record amendments as new auditable events.

---

### 27. SECURITY AND DATA INTEGRITY

Implement appropriate Odoo security groups:

- Trading Research Viewer.
- Trading Research Analyst.
- Trading Risk Manager.
- Trading System Administrator.

Implement:

- Model access controls.
- Record rules.
- Company isolation.
- Server-side authorization.
- Protected configuration.
- Secret redaction.
- Input validation.
- Safe SQL usage.
- Secure controller routes.
- Audit logging.
- Sensitive field restrictions.

Do not rely solely on frontend visibility for security.

Avoid unsafe unrestricted `sudo()` usage.

Do not expose broker tokens to ordinary users.

Use database constraints where required.

Test concurrent operations using genuinely independent transactions or processes.

Protect against duplicate ingestion, duplicate research runs, duplicate signals, and duplicate simulated executions.

Do not mutate real Odoo accounting records or real broker funds.

---

### 28. MANDATORY BUSINESS INVARIANTS

Preserve these invariants throughout all development:

- INV-01: No real broker order execution.
- INV-02: No mandatory paid AI dependency.
- INV-03: No GPU dependency.
- INV-04: No fabricated live market data.
- INV-05: No actionable signal from stale required data.
- INV-06: No look-ahead bias.
- INV-07: No future information in historical decisions.
- INV-08: No duplicate market data records.
- INV-09: No duplicate paper-trade execution.
- INV-10: No misleading profit guarantees.
- INV-11: No uncalibrated score represented as probability.
- INV-12: No unauthorized broker credential exposure.
- INV-13: No strategy promotion without validation.
- INV-14: No retrospective performance manipulation.
- INV-15: No silent synthetic-data substitution.
- INV-16: No ignoring material transaction costs in net returns.
- INV-17: No invalid position sizing.
- INV-18: No cross-company unauthorized access.
- INV-19: No risk veto overridden by signal score.
- INV-20: No forced daily trading recommendation.
- INV-21: No experimental strategy presented as validated.
- INV-22: No real account capital allocation.
- INV-23: No unbounded background processing.
- INV-24: No paper profit represented as real profit.
- INV-25: No test marked PASSED without execution evidence.
- INV-26: No unsupported market data entitlement bypass.
- INV-27: No missing required data treated as positive evidence.
- INV-28: No historical signal deletion to hide losses.
- INV-29: No dashboard KPI without a defined data source.
- INV-30: No production-readiness claim with unresolved critical blockers.

Create traceable tests for each applicable invariant.

---

### 29. REQUIRED TESTING PROGRAM

Implement and execute actual tests.

#### A. Python and Quantitative Tests

- Indicator mathematical correctness.
- Indicator warm-up.
- Candle validation.
- Missing values.
- Numerical precision.
- Strategy entry and exit rules.
- Risk calculations.
- Position sizing.
- Trading cost calculations.
- Expected value calculations.
- Statistical metrics.
- Probability calibration.
- Look-ahead bias prevention.
- Temporal feature correctness.

#### B. Odoo Tests

- Fresh installation.
- Module upgrade.
- Model registration.
- XML view validation.
- Menus and actions.
- Access rights.
- Record rules.
- Company isolation.
- Scheduled actions.
- Configuration persistence.
- Database constraints.

#### C. Broker Integration Tests

- Valid fixture authentication responses.
- Invalid credentials.
- Expired sessions.
- Rate limits.
- Network timeouts.
- WebSocket reconnect behavior.
- Invalid instrument tokens.
- Historical candle response validation.
- Stale quote detection.
- Real API smoke tests only when authorized credentials are available.

#### D. Trading Simulation Tests

- Paper account funding.
- Virtual cash reservation.
- Simulated buying.
- Simulated selling.
- Partial execution.
- Partial profit booking.
- Stop-loss execution.
- Trailing stop handling.
- Target execution.
- Intraday square-off.
- Insufficient virtual cash.
- Duplicate execution prevention.
- Concurrent execution prevention.
- Restart recovery.
- Realistic slippage.
- Same-candle target/stop ambiguity.

#### E. Research Validation Tests

- Chronological processing.
- Data leakage detection.
- Out-of-sample validation.
- Walk-forward evaluation.
- Benchmark comparison.
- Insufficient sample handling.
- Strategy rejection.
- Strategy suspension.
- Risk veto enforcement.
- Signal expiration.
- NO TRADE generation.

#### F. Real Browser UI Tests

Use a real running Odoo 20 Community instance and a supported browser testing method.

Verify:

- Dashboard rendering.
- Navigation.
- KPI accuracy.
- Filters.
- Sorting.
- Drill-downs.
- Stock detail pages.
- Chart rendering.
- Theme behavior.
- Responsive layout.
- Loading states.
- Empty states.
- Data error states.
- Stale-data alerts.
- Browser console errors.
- JavaScript exceptions.
- RPC failures.

Capture real screenshots where possible.

Do not use generated mockup images as browser testing evidence.

#### G. Performance Tests

Measure:

- RAM usage.
- CPU usage.
- Dashboard load time.
- Historical data ingestion speed.
- Research cycle duration.
- Indicator computation duration.
- Database query performance.
- Paper simulation throughput.

Evaluate suitable workloads, such as 50, 100, 250, and 500 instruments, subject to available data and resources.

Evaluate 1,000 instruments only if supported by the measured environment.

Record actual hardware, dataset size, configuration, duration, and resource usage.

#### H. Failure and Recovery Tests

Simulate:

- Internet disconnect.
- Broker failure.
- Invalid responses.
- Missing data.
- Stale data.
- Database operation failure.
- Research worker interruption.
- Application restart.
- Duplicate scheduled jobs.
- Partial ingestion.
- Memory pressure.
- Interrupted paper-trade processing.

Verify safe degradation and recovery.

---

### 30. MANDATORY ACCEPTANCE CRITERIA

Use these stable acceptance criteria:

- AC-001: Odoo 20 Community compatibility verified.
- AC-002: Fresh installation successful.
- AC-003: Module upgrades safely.
- AC-004: Zero mandatory paid AI APIs.
- AC-005: CPU-only operation.
- AC-006: 16 GB hardware optimization measured.
- AC-007: Secure provider configuration.
- AC-008: Instrument master synchronization.
- AC-009: Historical market data ingestion.
- AC-010: Authorized live market data integration.
- AC-011: Market data freshness enforcement.
- AC-012: Duplicate-data prevention.
- AC-013: Historical data provenance.
- AC-014: Correct indicator calculations.
- AC-015: Research engine interface operational.
- AC-016: Applicable research capabilities functional.
- AC-017: Versioned strategy framework.
- AC-018: Market regime detection.
- AC-019: Explainable master decision engine.
- AC-020: Transparent quality scoring.
- AC-021: Risk veto enforcement.
- AC-022: Transaction cost calculation.
- AC-023: Expected net return calculation.
- AC-024: Position sizing validation.
- AC-025: Signal freshness and expiry.
- AC-026: Historical backtesting.
- AC-027: Look-ahead bias prevention.
- AC-028: Out-of-sample validation.
- AC-029: Walk-forward testing.
- AC-030: Reproducible research experiments.
- AC-031: Automatic paper trading.
- AC-032: Virtual cash integrity.
- AC-033: Paper execution idempotency.
- AC-034: Paper portfolio reporting.
- AC-035: Strategy performance tracking.
- AC-036: Recommendation monitoring.
- AC-037: Automatic research scheduling.
- AC-038: Scheduler concurrency protection.
- AC-039: Premium dashboard operational.
- AC-040: Dashboard KPI correctness.
- AC-041: Real browser UI verified.
- AC-042: Security permissions verified.
- AC-043: Company isolation verified.
- AC-044: Credential redaction verified.
- AC-045: Recovery behavior verified.
- AC-046: No real-order functionality.
- AC-047: NO TRADE behavior verified.
- AC-048: No fabricated performance results.
- AC-049: Complete setup and user documentation.
- AC-050: Evidence-backed development report generated.

Do not mark acceptance criteria as passed solely because corresponding code exists.

---

### 31. EXECUTION PRIORITY FOR THIS DEVELOPMENT RUN

Execute in the following priority order:

Priority 0:

- Repository inspection.
- Actual environment verification.
- Requirements documentation.
- Architecture.
- Module foundation.
- Security.
- Configuration.
- Data models.
- Data provenance.
- Hard invariants.

Priority 1:

- Market data provider foundation.
- Historical data ingestion.
- Data quality.
- Indicator calculations.
- Initial research engines.
- Test infrastructure.

Priority 2:

- Strategy framework.
- Risk calculations.
- Cost calculations.
- Master decision engine.
- Backtesting foundation.
- Initial paper trading.

Priority 3:

- Functional premium dashboard.
- Research scanner.
- Research detail views.
- Paper portfolio.
- Scheduler.
- System health monitoring.

Priority 4:

- Additional validated strategies.
- Advanced statistics.
- Machine learning.
- Continuous improvement.
- Expanded dashboards.
- Performance optimization.

Complete as much verified development as the available environment and execution budget permit.

Prioritize correctness over feature count.

Do not stop after merely writing a plan.

Do not spend the entire execution on cosmetic UI while leaving the financial and data-quality foundations incorrect.

Preserve all future requirements in the traceability matrix.

---

### 32. MANDATORY DEVELOPMENT REPORT

At the end of this execution, create the following file in the module root:

`golok_ai_trading_lab_pro/DEVELOPMENT_REPORT.md`

This file is the authoritative handoff document for the next agentic development prompt.

It must be comprehensive, accurate, self-contained, and based on actual repository state and executed tests.

The report must include the following sections.

#### Section 01 — Executive Summary

- Product name.
- Current development milestone.
- Execution date.
- Current Git revision.
- Overall implementation status.
- Current readiness decision.
- Most important achievements.
- Most important unresolved risks.

#### Section 02 — Actual Environment

- Operating system.
- CPU model.
- Available RAM.
- GPU availability.
- Python version.
- PostgreSQL version.
- Odoo version.
- Odoo edition.
- Repository path.
- Addons path.
- Relevant dependency versions.
- Test database configuration, with secrets removed.

#### Section 03 — Architecture Implemented

- Actual directory tree.
- Implemented components.
- Component dependencies.
- Data flow.
- Research flow.
- Signal lifecycle.
- Paper-trade lifecycle.
- Security architecture.
- Architectural deviations and reasons.

#### Section 04 — Files Created and Modified

List all important created and modified files.

For each file include:

- Path.
- Purpose.
- Implementation status.
- Associated requirements.
- Important behavior.
- Remaining limitations.

#### Section 05 — Requirement Traceability Matrix

Include every mandatory requirement with:

| Requirement ID | Requirement | Status | Implementation Path | Test ID | Evidence | Remaining Work |
|---|---|---|---|---|---|---|

Allowed implementation statuses:

- COMPLETE.
- PARTIAL.
- NOT_STARTED.
- BLOCKED.
- DEFERRED_OUT_OF_SCOPE.

#### Section 06 — Research Engine Status

For RE-01 through RE-25 report:

- Implementation status.
- Mathematical method.
- Required data.
- Available data.
- Validation status.
- Test coverage.
- Known limitations.
- Signal eligibility.

#### Section 07 — Strategy Status

For every strategy report:

- Strategy ID.
- Version.
- Implementation status.
- Validation status.
- Historical dataset.
- Training period.
- Validation period.
- Final holdout period.
- Number of trades.
- Trading cost assumptions.
- Net results.
- Maximum drawdown.
- Limitations.
- Current eligibility.

Use NOT TESTED when evidence does not exist.

#### Section 08 — SmartAPI Integration Status

Document:

- Official sources consulted.
- Authentication implementation.
- Static IP findings.
- API entitlement findings.
- Rate-limit configuration.
- Historical integration status.
- Live integration status.
- WebSocket status.
- Actual live test evidence.
- Mock test evidence.
- Missing credentials or access blockers.
- Required owner setup steps.

Never include actual secrets.

#### Section 09 — Dashboard Development Status

For each dashboard report:

- Implementation status.
- Implemented KPIs.
- Calculation source.
- Working filters.
- Working drill-downs.
- Browser verification.
- Screenshot evidence.
- Known UI issues.
- Remaining development.

#### Section 10 — Complete Test Inventory

Include every executed and planned test.

Use:

| Test ID | Category | Test Description | Command | Expected Result | Actual Result | Status | Evidence |
|---|---|---|---|---|---|---|---|

Allowed test statuses:

- PASSED.
- FAILED.
- BLOCKED.
- SKIPPED.
- NOT_RUN.

PASSED requires actual successful execution.

Distinguish unit tests, integration tests, simulated provider tests, and real external integration tests.

#### Section 11 — Actual Test Execution Evidence

Include:

- Exact test commands.
- Exit codes.
- Test counts.
- Passed counts.
- Failed counts.
- Skipped counts.
- Execution duration.
- Relevant sanitized logs.
- Evidence file paths.

If a command failed, include the real failure reason and subsequent repair status.

Do not fabricate test output.

#### Section 12 — Business Invariant Verification

Report INV-01 through INV-30 individually.

Include implementation paths, verification method, test evidence, status, and remaining work.

#### Section 13 — Acceptance Criteria Verification

Report AC-001 through AC-050 individually.

Every criterion must have an explicit status.

A criterion may be marked passed only when all required evidence exists.

#### Section 14 — Financial Research Results

Include only actually measured results:

- Dataset provenance.
- Dataset size.
- Backtesting periods.
- Strategy performance.
- Trading costs.
- Net returns.
- Profit factor.
- Drawdowns.
- Sample sizes.
- Statistical uncertainty.
- Relevant limitations.

If no valid research experiment has been completed, state that clearly.

#### Section 15 — Performance Results

Include measured:

- CPU usage.
- RAM usage.
- Dataset sizes.
- Research durations.
- Ingestion durations.
- Dashboard timings.
- Database bottlenecks.
- Hardware limitations.

Distinguish measured performance from target performance.

#### Section 16 — Security Verification

Include:

- ACL results.
- Record rule results.
- Company isolation results.
- Credential protection.
- Secret scanning.
- Unauthorized operation tests.
- Real-order execution prohibition verification.
- Security issues and repairs.

#### Section 17 — Errors and Bug Fixes

For each significant issue include:

- Bug ID.
- Severity.
- Root cause.
- Affected components.
- Fix implemented.
- Regression test.
- Retest result.
- Remaining risk.

#### Section 18 — Incomplete Features

List every incomplete feature explicitly.

For each include:

- Requirement ID.
- Current state.
- Reason incomplete.
- Dependencies.
- Priority.
- Recommended next implementation.

#### Section 19 — Development Completion Metrics

Calculate implementation completion using the traceability matrix.

Report separate metrics for:

- Foundation.
- Market data.
- Research engines.
- Strategies.
- Statistical validation.
- Backtesting.
- Risk management.
- Paper trading.
- Dashboard.
- Automation.
- Security.
- Testing.
- Documentation.

Disclose the denominator and calculation method.

Do not guess a completion percentage.

Do not count unverified placeholders as completed features.

#### Section 20 — Next Development Recommendations

Provide a prioritized continuation plan containing:

- Critical blockers.
- Required repairs.
- Highest-value incomplete features.
- Dependencies.
- Missing tests.
- Performance improvements.
- Dashboard improvements.
- Research improvements.
- Suggested next milestone.
- Exact implementation paths relevant to continuation.

Do not require the next developer to rediscover information already known.

#### Section 21 — Owner Setup Instructions

Provide practical step-by-step instructions for:

- Installing dependencies.
- Starting Odoo.
- Installing the module.
- Configuring a paper trading account.
- Connecting authorized Angel One market data.
- Importing historical data.
- Running research.
- Opening the dashboard.
- Executing relevant tests.

#### Section 22 — Final Readiness Decision

Select the appropriate status:

- DEVELOPMENT INCOMPLETE.
- FOUNDATION VERIFIED.
- HISTORICAL RESEARCH READY.
- PAPER TRADING TEST READY.
- VERIFIED RESEARCH BETA.
- VALIDATED RESEARCH RELEASE READY.

Explain the decision with evidence.

Do not claim live trading readiness.

Do not claim production-quality signal accuracy without appropriate historical, out-of-sample, and prospective paper-trading evidence.

---

### 33. EVIDENCE ARTIFACTS

Create an appropriate evidence directory:

```text
docs/evidence/
    tests/
    installation/
    integration/
    browser/
    screenshots/
    quantitative/
    performance/
    security/
```

Store real evidence where available.

Ensure evidence contains no passwords, API keys, TOTP secrets, private account identifiers, or authentication tokens.

Reference these artifacts from DEVELOPMENT_REPORT.md.

Create an evidence manifest with file paths and SHA-256 hashes where practical.

A missing artifact must be reported as missing.

---

### 34. NON-NEGOTIABLE QUALITY RULES

- No fabricated development results.
- No fabricated test results.
- No fabricated API integration results.
- No fabricated research performance.
- No fabricated live market prices.
- No fabricated historical statistics.
- No hidden incomplete features.
- No misleading completion percentage.
- No unsupported profit guarantee.
- No fake premium dashboard.
- No unauthorized broker operation.
- No real-money trading.
- No paid AI dependency.
- No unnecessary GPU dependency.
- No unsafe secrets.
- No ignored critical errors.
- No unverified release-readiness declaration.

Resolve discovered bugs whenever possible.

After each significant repair, execute the relevant regression tests again.

If a test cannot be executed, report the specific blocker.

---

### 35. FINAL EXECUTION INSTRUCTION

Begin actual development now.

Inspect the environment, establish the architecture, implement the highest-priority functional components, execute relevant tests, repair discovered defects, verify the real Odoo interface where possible, and create the complete DEVELOPMENT_REPORT.md.

Do not finish with only a textual development plan.

At the end, print a concise terminal summary containing:

```text
PROJECT: Golok AI Trading Lab Pro
CURRENT MILESTONE:
IMPLEMENTED COMPONENTS:
PARTIAL COMPONENTS:
TESTS PASSED:
TESTS FAILED:
TESTS BLOCKED:
TESTS NOT RUN:
CRITICAL BLOCKERS:
IMPLEMENTATION COMPLETION:
VERIFICATION COMPLETION:
CURRENT READINESS:
DEVELOPMENT REPORT PATH:
NEXT RECOMMENDED MILESTONE:
```

Print only actual measured counts and statuses.

The complete DEVELOPMENT_REPORT.md will be submitted to an independent technical reviewer who will prepare the next development prompt based on the actual development state.

Build the strongest possible foundation.

Prioritize mathematical correctness, trustworthy data, realistic simulations, capital protection, explainability, premium user experience, and verified engineering quality.

END OF MASTER DEVELOPMENT PROMPT 01.

---

## P02 specification addition

# GOLOK AI TRADING LAB PRO

## MASTER AGENTIC DEVELOPMENT PROMPT 02 — VERIFIED MARKET INTELLIGENCE, PROFESSIONAL QUANTITATIVE RESEARCH, COST-AWARE BACKTESTING AND PREMIUM DASHBOARD

### 1. Mission and Engineering Authority

Act as a multidisciplinary senior engineering and institutional quantitative research team responsible for continuing the actual development of Golok AI Trading Lab Pro.

Your responsibilities include:

- Principal Odoo 20 Community architecture.
- Financial market data engineering.
- Quantitative trading research.
- Mathematical and statistical correctness.
- Python performance engineering.
- Angel One SmartAPI integration.
- Financial risk management.
- Historical strategy validation.
- Native OWL frontend development.
- Professional financial dashboard design.
- PostgreSQL integrity and concurrency.
- Application security.
- Automated testing.
- Evidence-driven quality assurance.

Implement actual working software, execute actual tests, repair discovered defects, and produce a complete development handoff.

Do not return only a development plan.

This is an iterative development milestone, not an unconditional final release.

---

### 2. Mandatory Source Documents

Before modifying anything, read the complete contents of:

- `DEVELOPMENT_REPORT.md`
- `docs/MASTER_REQUIREMENTS.md`
- `docs/REQUIREMENTS_TRACEABILITY.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT_PLAN.md`
- `docs/DECISION_LOG.md`
- `docs/RISK_REGISTER.md`
- `README.md`

Inspect the existing source code, tests, scripts, screenshots and evidence artifacts.

The original MASTER_REQUIREMENTS.md remains the governing product specification.

Preserve every existing:

- RE-01 through RE-25 research capability identifier.
- ST-01 through ST-20 strategy identifier.
- INV-01 through INV-30 business invariant.
- AC-001 through AC-050 acceptance criterion.
- Existing S-series traceability identifier.
- Previously implemented and verified behavior.

Do not remove requirements simply because they are difficult or currently blocked.

Where this prompt introduces additional requirements, assign stable P02-specific identifiers.

---

### 3. Known Development Baseline

The previous development report states:

- Readiness: FOUNDATION VERIFIED for the historical descriptive research slice.
- Applicable requirements: 1,236.
- Complete requirements: 72.
- Requirements coverage: approximately 5.83%.
- Acceptance criteria passed: 14 of 50.
- Named test inventory: 24 PASSED, 0 FAILED, 1 BLOCKED, 70 NOT_RUN and 29 grouped coverage references.
- Research engines: RE-01, RE-05 and RE-18 partially implemented.
- Other research engines: not started.
- Trading strategies: none implemented.
- Financial research experiments: none completed.
- Existing decision output: historical NO TRADE.
- Broker adapter: not implemented.
- Paper trading: not implemented.
- Dashboard: initial OWL overview and native record views.

These are reported baseline results, not independent proof.

Reconcile them against actual repository files and original test artifacts.

Do not blindly inherit previous PASSED statuses.

---

### 4. Actual Target Environment

The previous report detected:

- Windows NT 10.0.26300.0.
- Intel Core i5-10210U.
- Four physical CPU cores.
- Eight logical processors.
- Approximately 16 GB RAM.
- Approximately 3.4 GiB available RAM at inspection.
- Intel UHD integrated graphics.
- No dedicated GPU.
- Python 3.14.6 in the Odoo virtual environment.
- PostgreSQL 18.4.
- Odoo 20 Community.
- Module path: `C:/PycharmProjects/odoo20/custom_addons/golok_ai_trading_lab_pro`.

Verify these details again before execution.

The application must remain fully functional without:

- Paid AI APIs.
- Local LLMs.
- Ollama.
- GPU acceleration.
- Paid cloud computing.
- Mandatory paid analytics subscriptions.

Prefer Python standard-library implementations when sufficient.

Add numerical or machine learning dependencies only when justified, compatible with the installed Python version, and supported by measurable benefits.

Do not downgrade or modify the owner's Odoo environment without explicit authorization.

---

### 5. Absolute Real-Money Trading Prohibition

The current product remains a research and simulation platform.

The owner manually executes any actual trades outside the application.

The application MUST NOT contain:

- Real order placement.
- Real order modification.
- Real order cancellation.
- Automatic real-money buying.
- Automatic real-money selling.
- Automatic allocation of real account balances.
- Fund transfer functionality.
- Hidden real-order execution services.
- Dormant autonomous trading code.

Angel One integration must be restricted to authorized authentication and read-only market data access.

Paper trading must remain completely isolated from real broker execution.

No real Odoo accounting entries may be created or mutated.

Do not implement the previously discussed automatic 25% capital allocation feature.

That feature remains explicitly outside the current project scope.

---

### 6. Phase P02-A — Baseline Preservation and Independent Audit

Assign audit identifiers AUD-001 onward.

Before adding new features:

1. Inspect the complete module source.
2. Inspect all existing database models and constraints.
3. Verify existing security groups and company domains.
4. Review every existing public RPC-callable method.
5. Inspect the previous evidence manifest.
6. Verify referenced evidence paths and hashes.
7. Inspect historical failure logs and subsequent repairs.
8. Re-execute the previous standalone tests.
9. Re-execute the Odoo integration tests.
10. Re-execute the independent database contention test.
11. Re-execute the real browser test suite.
12. Identify regressions and hidden incomplete implementations.
13. Repair confirmed defects before building dependent features.

Pay particular attention to the previous fixes:

- BUG-01: Odoo 20 `ir.access` migration.
- BUG-02: Odoo 20 BinaryValue handling.
- BUG-03: Sass compatibility.
- BUG-04: OWL 3 reactivity and template scope.
- ENV-01: Isolated PostgreSQL harness execution.

Do not reintroduce legacy Odoo APIs.

Inspect the local Odoo source for supported implementation patterns.

Preserve existing XML IDs and installed data compatibility.

---

### 7. Version Control and Evidence Integrity

The previous report states that the module workspace has no Git repository.

Inspect the parent directory and module directory before making changes.

If a valid Git repository exists, use its existing workflow.

If none exists:

- Create a non-destructive source baseline manifest with SHA-256 hashes.
- Establish a recoverable local source checkpoint.
- Exclude credentials, test database contents, virtual environments, runtime logs and private market data.
- Document an appropriate version-control setup.

Do not overwrite an existing repository or publish source code remotely.

Preserve the previous development report as:

`docs/history/DEVELOPMENT_REPORT_P01.md`

Preserve previous evidence separately from new execution evidence.

Never present old test output as newly executed output.

---

### 8. Traceability Correction

Audit the existing requirements matrix for semantic errors and inconsistent statuses.

The previous report contains entries such as:

- Place real broker orders — COMPLETE.
- Modify real broker orders — COMPLETE.
- Automatically buy real shares — COMPLETE.

These refer to prohibited functionality, not implemented capabilities.

Correct their descriptions while preserving stable identifiers:

- Real broker order placement is prohibited and absent.
- Real broker order modification is prohibited and absent.
- Automatic real-money buying is prohibited and absent.

Distinguish between:

- A working verified capability.
- A partially implemented capability.
- A mandatory prohibition.
- An unavailable external dependency.
- An optional technology.
- A future out-of-scope feature.
- A guard that currently holds only because the underlying feature does not exist.

Do not count optional libraries such as NumPy, Pandas or XGBoost as mandatory missing functionality merely because they are not installed.

Do not inflate completion percentages by counting a future risk-control feature as verified when no relevant risk engine exists.

Report separately:

1. Functional capability coverage.
2. Mandatory constraint compliance.
3. Acceptance criteria verification.
4. Test execution coverage.
5. External integration verification.
6. Financial strategy validation.

Preserve the original 72/1,236 baseline for historical comparison.

If the denominator changes, explain every change and provide a comparable baseline metric.

---

### 9. Phase P02-B — Exchange Trading Calendar and Point-in-Time Data

Create a verified exchange-aware calendar service.

Support NSE and BSE equity sessions where reliable source information is available.

Implement:

- Exchange identifiers.
- Trading dates.
- Standard trading sessions.
- Pre-open session distinctions.
- Market holidays.
- Weekends.
- Special trading sessions.
- Session opening and closing timestamps.
- Intraday entry cutoff configuration.
- Intraday exit cutoff configuration.
- Session versioning.
- Calendar source provenance.
- Calendar verification date.
- Asia/Kolkata display semantics.
- UTC storage semantics.

Verify official exchange documentation and circulars before treating calendar records as authoritative.

Do not assume every weekday is a trading day.

Do not assume every trading session has identical hours.

Support explicit timestamp semantics for candle opening and closing times.

Prevent:

- Candles outside authorized sessions.
- Candles spanning invalid session boundaries.
- Future-dated closed candles.
- Research from incomplete candles.
- Incorrect aggregation across overnight boundaries.
- Incorrect daily candle assignment.
- Incorrect holiday gap classification.

For historical point-in-time research, distinguish:

- Market event time.
- Candle opening time.
- Candle closing time.
- Source publication or availability time.
- Application ingestion time.
- Research decision time.

A historical observation may only be used when it would have been available at the simulated decision time under the documented source semantics.

If point-in-time availability cannot be established, explicitly record the limitation and block inappropriate validation claims.

Provide dedicated calendar unit tests and real ORM integration tests.

---

### 10. Instrument Reference Intelligence

Extend the existing instrument model without breaking historical references.

Implement:

- Exchange.
- Trading symbol.
- Provider-specific token mapping.
- ISIN where available.
- Instrument type.
- Trading segment.
- Tick size.
- Lot size.
- Listing status.
- Effective date.
- Suspension status.
- Delisting status.
- Sector classification.
- Reference data source.
- Mapping version.
- Mapping verification state.

Support effective-dated symbol and token changes.

Do not identify instruments solely by a mutable trading symbol.

Prevent incorrect provider token reuse from contaminating historical records.

Support documented split and bonus adjustment metadata.

Keep adjusted and unadjusted prices distinct.

Never mix adjustment conventions inside an experiment.

If corporate action or historical universe information is unavailable, mark the applicable survivorship and adjustment checks as incomplete.

Do not invent delisting, sector or corporate action information.

---

### 11. Market Data Quality V2

Extend the existing `services/market_data.py`, ORM models and import wizard using a clean modular structure.

Preserve:

- Decimal price precision.
- Immutable candle records.
- Existing conflict detection.
- Existing idempotent import behavior.
- Historical research snapshot digests.
- Company isolation.

Add:

- Explicit source classifications.
- Historical versus live data classification.
- Delayed data classification.
- Synthetic fixture classification.
- Dataset authorization status.
- Source verification status.
- Session-aware missing candle detection.
- Candle completeness checks.
- Data freshness checks.
- Quote age checks.
- Sequence or timestamp ordering checks.
- Provider schema validation.
- Data quality issue records.
- Dataset quarantine.
- Provider outage detection.
- Controlled recovery.

Implement a validated data eligibility contract.

Separate:

- Structurally valid data.
- Calendar-valid data.
- Source-verified data.
- Point-in-time eligible data.
- Research-only data.
- Live decision-eligible data.

An operator-entered source name must not automatically establish source authenticity.

Do not silently replace a verified dataset with synthetic or delayed data.

The system must default to NO TRADE when mandatory data eligibility checks fail.

Extend independent PostgreSQL contention tests to cover overlapping imports, conflicting values, transaction rollback and safe retries.

---

### 12. Phase P02-C — Angel One SmartAPI Read-Only Integration

Create a narrow provider interface under `services/providers/` or an equivalent documented modular structure.

Use official Angel One documentation and the official SDK repository.

References:

- https://smartapi.angelone.in/
- https://smartapi.angelone.in/docs
- https://github.com/angel-one/smartapi-python

Recheck:

- Account-specific pricing.
- Market data entitlements.
- Static IP requirements.
- Personal use restrictions.
- Data storage and redistribution restrictions.
- Authentication requirements.
- Session expiration.
- REST rate limits.
- WebSocket limits.
- Historical lookback limits.
- Supported instrument types.

The previous report could not confirm all current limits.

Do not hardcode guessed limits.

Where authoritative limits remain unavailable, use explicitly documented conservative request caps and block unrestricted operation.

Implement a provider capability registry.

Implement, where supported and authorized:

- Protected provider configuration.
- Authentication.
- Session lifecycle.
- Controlled reauthentication.
- Instrument master synchronization.
- Historical candle retrieval.
- Live quote retrieval.
- Read-only WebSocket subscriptions.
- Heartbeat monitoring.
- Connection state management.
- Exponential backoff.
- Bounded retries.
- Timeout handling.
- Rate-limit enforcement.
- Schema error handling.
- Connectivity diagnostics.
- Last successful request tracking.
- Subscription count monitoring.
- Data lag tracking.

Use an explicit outbound endpoint allowlist.

Do not expose arbitrary broker endpoint execution.

Do not implement any order-related endpoint.

Avoid installing an unrestricted SDK unnecessarily. If the SDK is used, isolate it behind a narrow read-only adapter and enforce outbound operation restrictions.

Use environment secrets or an appropriately protected Windows-compatible secret store.

Prevent secrets from appearing in:

- Database-readable configuration fields.
- Browser responses.
- HTTP diagnostics.
- Screenshots.
- Test artifacts.
- Source code.
- Exceptions.
- Development reports.

Without authorized credentials:

- Implement and execute deterministic fixture integration tests.
- Keep real network integration disabled.
- Mark live smoke tests BLOCKED.
- Continue developing independent functionality.

Do not classify development of the adapter itself as blocked merely because owner credentials are absent.

No paid service may be activated without owner authorization.

---

### 13. Provider Failure and Safe Degradation

Create provider health states:

- NOT_CONFIGURED.
- AUTH_REQUIRED.
- CONNECTING.
- CONNECTED.
- DEGRADED.
- RATE_LIMITED.
- STALE.
- DISCONNECTED.
- BLOCKED.
- ERROR.

Record transitions with timestamps and sanitized diagnostic reasons.

A connection status of CONNECTED must not be treated as proof that every instrument has fresh data.

Implement per-instrument freshness.

When a provider becomes unavailable:

- Block new actionable recommendations.
- Invalidate affected recommendations where applicable.
- Stop generating simulated fills from stale prices.
- Preserve existing records.
- Allow authorized historical research to continue independently.
- Clearly display the failure on the dashboard.

Do not bypass static IP, authentication or market data access restrictions.

---

### 14. Phase P02-D — Complete Technical Indicator Library

Expand the three existing descriptive indicators into a professional independently testable quantitative library.

Implement and verify:

- SMA.
- EMA.
- RSI.
- MACD.
- ATR.
- VWAP.
- ADX.
- Bollinger Bands.
- Stochastic Oscillator.
- Relative Volume.
- Rate of Change.
- On-Balance Volume.
- Historical Volatility.
- Rolling Highs and Lows.
- Opening Range.
- Relative Strength.
- Price Gaps.
- Volume Spikes.
- Trend Slopes.

Each indicator must define:

- Mathematical formula.
- Algorithm version.
- Input requirements.
- Warm-up period.
- Null and missing-value policy.
- Numerical precision.
- Timeframe semantics.
- Session behavior.
- Expected output.
- Invalid-input behavior.

Special requirements:

- VWAP resets per applicable session.
- Opening range cannot be known before its configured window closes.
- Breakout levels must exclude future bars.
- Relative volume must use a documented baseline.
- Relative strength requires a properly aligned benchmark.
- Rolling statistics must not include future observations.
- Zero-volume and zero-denominator cases must be handled explicitly.
- ATR and RSI smoothing must match documented conventions.
- Standard deviation conventions must be declared.
- Warm-up values must remain unavailable rather than silently defaulting to zero.

Support appropriate 1, 3, 5, 15 and 30-minute, hourly and daily intervals.

Implement session-aware aggregation where necessary.

Do not produce artificial higher-frequency candles by interpolating lower-frequency observations.

Verify indicator results against independent reference calculations.

Use hand-calculated fixtures for critical mathematical cases.

Implement prefix-invariance tests: appending future candles must not change previously calculated causal results.

---

### 15. Professional Research Engine Contract

Implement a versioned framework for RE-01 through RE-25.

Every research result must provide:

- Engine ID.
- Engine version.
- Instrument.
- Dataset identity.
- Research timestamp.
- Decision cutoff.
- Required input fields.
- Data source and freshness.
- Findings.
- Supporting evidence.
- Contradictory evidence.
- Missing inputs.
- Limitations.
- Applicable strategies.
- Execution duration.
- Result status.
- Input digest.

Use statuses:

- COMPLETED.
- NOT_APPLICABLE.
- INSUFFICIENT_DATA.
- STALE_DATA.
- ERROR.

Prioritize actual implementation of OHLCV-supported research:

- RE-01 Technical Analysis.
- RE-03 Price Action.
- RE-04 Candlestick Patterns.
- RE-05 Volume Intelligence.
- RE-06 Support and Resistance.
- RE-07 Breakout Detection.
- RE-08 False Breakout Detection.
- RE-09 Market Trend.
- RE-15 Historical Patterns.
- RE-17 Liquidity Analysis, explicitly limited to available proxies.
- RE-18 Volatility.
- RE-19 Momentum.
- RE-20 Abnormal Market Activity.

Implement benchmark and sector research only when compatible input data is available.

Do not fabricate financial statements, news, global market data or institutional activity.

Do not present an empty engine implementation as completed.

External-data-dependent engines must remain accurately classified until their data foundations exist.

Never convert missing research evidence into positive scores.

---

### 16. Phase P02-E — Professional Transaction Cost Engine

Implement an effective-dated Indian equity transaction cost framework.

Support:

- Brokerage.
- Securities Transaction Tax.
- Exchange transaction charges.
- Applicable SEBI charges.
- GST.
- Stamp duty.
- Bid-ask spread.
- Slippage.
- Other verified applicable charges.

Every tariff must contain:

- Effective start date.
- Effective end date when applicable.
- Exchange.
- Trading segment.
- Transaction side.
- Charge basis.
- Rate or fixed amount.
- Minimum or maximum charge if applicable.
- Rounding method.
- Official source.
- Verification status.

Consult authoritative broker and regulatory sources.

Do not invent current charges.

Where verified historical tariffs are unavailable, permit explicitly labeled hypothetical cost configurations for simulation only.

Implement Decimal-safe calculations.

Support entry and exit charges independently.

Distinguish between:

- Gross trading P&L.
- Brokerage.
- Statutory charges.
- Execution friction.
- Net trading P&L.

Prevent double-counting spread or slippage when execution prices already incorporate them.

Add tests for:

- Small trades.
- Large trades.
- Different buy/sell charges.
- Tariff effective-date boundaries.
- Rounding.
- Zero and invalid quantities.
- Missing tariff information.
- Negative net profit despite positive gross profit.

Do not enable actionable real-market recommendations without sufficient cost information.

---

### 17. Phase P02-F — Independent Risk Management Foundation

Implement a risk service independent of the research score.

Use configurable initial simulation defaults:

- Virtual reference capital: INR 50,000.
- Planned per-trade risk: 0.5%.
- Planned daily loss threshold: 1%.
- Minimum net planned reward-to-risk ratio: 2:1.
- Preferred candidate reward-to-risk: 3:1.
- Maximum daily paper entries: 3.
- Consecutive loss pause threshold: 2.
- No leverage.
- No averaging losing positions.
- No martingale.
- No short strategy activation at this milestone.

These are initial research parameters, not proven optimal settings.

Implement:

- Capital-aware position sizing.
- Fee-aware position sizing.
- Stop-loss validation.
- Target validation.
- Tick-size validation.
- Quantity validation.
- Liquidity-based sizing restrictions.
- Maximum planned risk validation.
- Estimated adverse execution allowance.
- Minimum net reward-to-risk validation.
- Independent risk veto.
- Structured risk rejection reasons.

Evaluate complete position economics.

For a simulated long position, planned loss must account for entry-to-stop price loss and estimated entry/exit costs.

Planned net reward must account for entry-to-target price gain less estimated costs.

Quantity must satisfy both capital and risk limits after applicable costs.

Return a zero-quantity rejection when no valid position can be formed.

Do not widen a stop loss merely to obtain a favorable research score.

Do not move a target to an unrealistic level merely to meet reward-to-risk requirements.

Stop-loss controls must not be described as guaranteed maximum losses.

---

### 18. Phase P02-G — Versioned Strategy Framework

Implement the strategy framework required by the original MASTER_REQUIREMENTS.md.

Each strategy version must preserve:

- Strategy ID.
- Version.
- Code or implementation digest.
- Parameter configuration.
- Applicable market regime.
- Required indicators.
- Required data.
- Entry conditions.
- Exit conditions.
- Stop methodology.
- Target methodology.
- Risk policy.
- Expiry policy.
- Research validation state.

Use explicit states such as:

- DRAFT.
- RESEARCH_ONLY.
- BACKTESTED.
- VALIDATION_FAILED.
- VALIDATION_BLOCKED.
- PAPER_EVALUATION.
- SUSPENDED.

Do not implement automatic promotion.

All strategies must remain ineligible for actionable real-market recommendations during this milestone.

---

### 19. First Complete Strategy Candidate — ST-01 Opening Range Breakout

Implement one complete, explainable, long-only research strategy.

The goal is to establish an end-to-end tested research workflow, not to claim profitability.

Define and version:

- Opening range duration.
- Eligible trading session.
- Breakout confirmation method.
- Volume confirmation method.
- Optional trend confirmation.
- Maximum acceptable entry deviation.
- Entry cutoff.
- Stop-loss methodology.
- Target methodology.
- Maximum holding period.
- Session exit policy.
- False-breakout invalidation.
- Risk restrictions.
- Cost restrictions.

Opening range calculations must use only completed eligible candles.

Do not generate a simulated entry before the opening range is known.

A decision generated from a candle close must not receive an impossible earlier fill.

Implement:

- Qualifying breakout.
- Unconfirmed breakout.
- Insufficient opening range data.
- Low-volume rejection.
- Excessive volatility rejection.
- Late-session rejection.
- Invalid data rejection.
- Risk rejection.
- Cost rejection.
- Expired candidate rejection.

Record all considered candidates, including rejected and losing candidates.

Do not select parameters retrospectively to create a successful historical demonstration.

If ST-01 is fully implemented and verified, additional candidates such as ST-02 VWAP Pullback may be started only after higher-priority work is stable.

---

### 20. Phase P02-H — Historical Backtesting Foundation

Implement a real chronological backtesting engine.

Reuse the same indicator, strategy, cost and risk implementations intended for future paper research.

Prevent separate inconsistent formulas between modules.

Required execution behavior:

1. Load an explicitly identified dataset.
2. Validate dataset eligibility.
3. Iterate observations chronologically.
4. Generate a decision using available information.
5. Simulate entry only after decision availability.
6. Apply capital and risk checks.
7. Apply realistic execution assumptions.
8. Monitor stop and target conditions.
9. Close simulated positions according to policy.
10. Record gross and net outcomes.
11. Calculate reproducible experiment results.

Implement conservative handling of:

- Price gaps through stops.
- Gap openings beyond target prices.
- Same-candle target/stop ambiguity.
- Entry and exit ambiguity.
- Missing market data.
- Incomplete candles.
- Illiquid observations.
- Suspended instruments.
- Session closing.
- Insufficient capital.
- Transaction costs.
- Slippage.

When both stop and target are crossed and the true execution sequence is unknown, apply the documented conservative policy.

Do not assume the favorable result.

Do not fill a simulated order merely because a historical candle touched a price when realistic execution cannot be justified.

Record unresolved execution assumptions.

---

### 21. Financial Research Metrics

Implement:

- Total simulated trades.
- Winning trades.
- Losing trades.
- Neutral trades.
- Gross profit.
- Gross loss.
- Total costs.
- Net P&L.
- Average net trade.
- Win rate.
- Profit factor.
- Maximum drawdown.
- Equity curve.
- Consecutive losses.
- Net expectancy.
- Maximum adverse excursion where supported.
- Maximum favorable excursion where supported.

Handle zero denominators and empty trade samples correctly.

Return unavailable or insufficient evidence rather than misleading numerical defaults.

Separate all outputs by dataset, strategy version, experiment and validation partition.

Never present synthetic fixture results as financial performance evidence.

---

### 22. Historical Validation and Anti-Overfitting

Establish an immutable experiment specification before execution.

Include:

- Dataset identifiers and hashes.
- Universe selection rules.
- Strategy version.
- Parameter configuration.
- Cost schedule.
- Risk configuration.
- Execution model.
- Training period.
- Validation period.
- Final holdout period.
- Benchmark.
- Predeclared performance acceptance rules.

Implement chronological dataset partitioning.

Where appropriate, apply purging or embargo between samples whose outcome windows overlap.

Prevent:

- Random splitting that leaks future market information.
- Parameter tuning on the final holdout.
- Survivorship bias misrepresentation.
- Corporate action contamination.
- Repeated holdout selection.
- Selective omission of failed experiments.

Prepare walk-forward validation infrastructure.

Run experiments on authorized historical data if available.

If unavailable:

- Execute deterministic synthetic correctness tests.
- Mark financial validation as BLOCKED.
- Do not publish win-rate or profitability claims.

Keep sample-size requirements and strategy evaluation thresholds explicit.

A profitable backtest alone does not authorize real-market recommendations.

---

### 23. Master Decision Engine V2 — Fail-Closed Architecture

Extend the current historical NO TRADE behavior into a structured decision pipeline.

Required decision gates:

- G01: Source eligibility.
- G02: Instrument eligibility.
- G03: Trading session validity.
- G04: Candle completeness.
- G05: Market data freshness.
- G06: Research input sufficiency.
- G07: Strategy implementation status.
- G08: Strategy validation status.
- G09: Cost model availability.
- G10: Position sizing.
- G11: Independent risk veto.
- G12: Decision expiry.
- G13: Evidence integrity.
- G14: Research-mode restrictions.

All applicable hard gates must pass before a candidate can qualify for its permitted research or simulation mode.

Keep actionable real-market recommendations disabled throughout P02.

Allow:

- Historical descriptive results.
- WATCH observations.
- RESEARCH CANDIDATE results.
- BACKTEST CANDIDATE results.
- Explicit simulation candidates.
- NO TRADE.
- INVALIDATED.
- EXPIRED.

These states must be visually distinct from a validated actionable BUY or SELL recommendation.

Record every rejection reason.

Do not create artificial 90+ quality scores.

If scoring is implemented, store its decomposition and label it as experimental and uncalibrated.

---

### 24. Phase P02-I — Atomic Paper Trading Foundation

After cost, risk and backtesting foundations pass their targeted tests, implement the initial virtual trading ledger.

Default configurable virtual balance: INR 50,000.

Prioritize:

- Virtual account creation.
- Opening balance.
- Available cash.
- Reserved virtual cash.
- Simulated order lifecycle.
- Simulated fill lifecycle.
- Long virtual positions.
- Closed virtual positions.
- Transaction costs.
- Realized virtual P&L.
- Unrealized virtual P&L.
- Immutable virtual ledger events.
- Trading journal.

Use explicit simulation-only identifiers and labels.

Enforce accounting invariants:

- Available cash cannot become negative.
- Reserved cash cannot become negative.
- Filled quantity cannot exceed permitted quantity.
- Closed quantity cannot exceed open quantity.
- Duplicate fills cannot change balances twice.
- The virtual ledger must reconcile with cash, positions and realized P&L.
- All material balance changes must be auditable.
- Failed database transactions must not leave partial state.

Use independent transactions for contention tests.

Handle idempotent retry and application restart.

Separate historical replay simulation from prospective paper trading.

Do not automatically activate prospective paper trading until its data, execution and risk prerequisites are established.

If time or environment limitations prevent completing this phase, preserve the working earlier phases and report the exact remaining work.

Do not create placeholder financial records simply to display impressive dashboard balances.

---

### 25. Phase P02-J — Premium Native Odoo Trading Dashboard V2

Upgrade the existing historical overview into a professional financial research terminal.

Preserve the existing functional views and native drill-downs.

Use verified Odoo 20 OWL 3 patterns.

Do not use unsupported OWL 2 examples.

#### Visual Design Requirements

Create a premium Golok Technology financial analytics workspace featuring:

- Clean professional typography.
- Compact financial KPI cards.
- Consistent spacing and alignment.
- Responsive desktop and mobile layout.
- Professional light and dark theme compatibility.
- Subtle neutral surfaces.
- Blue accent for research and navigation.
- Green and red for actual positive and negative financial outcomes.
- Amber for uncertainty, staleness and warnings.
- Accessible status labels.
- Clear data timestamps.
- Fast and bounded chart rendering.

Avoid fake statistics, distracting animation and unnecessary decorative graphics.

Use actual server-backed values.

#### Dashboard Header

Display:

- Golok AI Trading Lab Pro.
- Current company.
- Current research mode.
- Market session state.
- Market data provider state.
- Last successful update.
- Data freshness.
- Research readiness state.

Prominently display:

RESEARCH / SIMULATION ONLY — NOT CONNECTED TO REAL ORDER EXECUTION.

#### Dashboard Section A — Market Data Intelligence

Display available verified values:

- Registered instruments.
- Eligible instruments.
- Active datasets.
- Stored candles.
- Validated candles.
- Quarantined datasets.
- Data quality issues.
- Missing observations.
- Provider connectivity.
- Last ingestion time.

Unavailable market indices and breadth metrics must be displayed as unavailable, not zero or fictional.

#### Dashboard Section B — Professional Research Scanner

Provide:

- Searchable stock table.
- Exchange filter.
- Dataset filter.
- Research state filter.
- Timeframe filter.
- Data quality filter.
- Strategy candidate filter.
- Last research timestamp.
- Research duration.
- Rejection reasons.

Implement pagination and server-side filtering.

Avoid loading the complete market universe into the browser.

#### Dashboard Section C — Stock Research Terminal

Provide a functional instrument detail screen containing:

- OHLC candlestick chart.
- Volume chart.
- Available SMA and EMA overlays.
- VWAP overlay when applicable.
- Opening range visualization.
- Support and resistance observations where implemented.
- Indicator values.
- Research result cards.
- Supporting and contradictory evidence.
- Data quality information.
- Historical decision cutoff.
- Dataset provenance.

Use actual stored historical data.

Bound the number of displayed candles.

Do not use synthetic chart values unless the entire dataset and view are explicitly labeled as synthetic.

#### Dashboard Section D — Strategy Research Laboratory

Display:

- Registered strategy versions.
- Implemented strategies.
- Research-only status.
- Backtest experiments.
- Validation status.
- Sample sizes.
- Dataset provenance.
- Net experiment results.
- Drawdown.
- Costs.
- Rejection reasons.

Display NOT TESTED when no experiment exists.

#### Dashboard Section E — Paper Trading

If the virtual ledger has been genuinely implemented:

- Virtual starting capital.
- Available virtual cash.
- Reserved virtual cash.
- Open virtual positions.
- Virtual equity.
- Realized virtual P&L.
- Unrealized virtual P&L.
- Trade history.

Otherwise, display a clear unavailable state.

Do not display invented zero-balance or INR 50,000 account records as if an account exists.

#### Dashboard Section F — System Health

Display available:

- Provider connection state.
- Last successful synchronization.
- API error state.
- Data lag.
- Research job state.
- CPU usage.
- RAM usage.
- Storage usage.
- Last research duration.

Expose only authorized, sanitized diagnostics.

#### Dashboard Section G — Readiness Center

Display evidence-backed readiness gates for:

- Data quality.
- Provider integration.
- Research engines.
- Cost engine.
- Risk engine.
- Backtesting.
- Paper trading.
- Security.
- Real-market recommendation eligibility.

A failed or incomplete readiness gate must be visible.

Provide authorized drill-downs.

All dashboard KPIs must have documented calculation definitions.

---

### 26. CPU and Memory Performance Engineering

Optimize specifically for Intel Core i5-10210U and 16 GB RAM.

The previous inspection showed limited immediately available RAM.

Implement:

- Bounded dataset reads.
- Chunked ingestion.
- Bounded indicator windows.
- Efficient indexes.
- Configurable batch sizes.
- Limited worker concurrency.
- Bounded caching.
- Research timeouts.
- Memory-pressure checks.
- Safe job cancellation.
- Persistent checkpoints where scheduling is implemented.

Avoid concurrent heavy research by default.

Measure available memory before starting large workloads.

Do not rely solely on Python `tracemalloc` measurements.

Measure process RSS, system available RAM and CPU utilization.

Include Odoo and PostgreSQL resource usage where practical.

Benchmark actual end-to-end workloads using 50, 100, 250 and 500 instruments when resources and authorized datasets permit.

Distinguish synthetic workloads from actual market datasets.

Record:

- Number of instruments.
- Candles per instrument.
- Dataset size.
- Database operations.
- Query latency.
- Total research duration.
- Process memory.
- System memory.
- CPU utilization.
- Browser response latency.

The previous 500-instrument result of approximately 14.1 seconds measured only descriptive service execution.

Do not reuse it as evidence of complete stock scanner performance.

Attempt a 1,000-instrument workload only if smaller measured workloads justify it.

---

### 27. Background Job Foundation

If the prerequisite data and research services are stable, implement a lightweight Odoo-native job framework.

Support:

- Unique job identity.
- Job type.
- Company scope.
- Requested timestamp.
- Execution status.
- Start and completion timestamps.
- Retry count.
- Failure reason.
- Checkpoint.
- Maximum runtime.
- Cancellation state.

Implement:

- Database-backed duplicate prevention.
- Independent transaction locking.
- Bounded job execution.
- Recovery of interrupted jobs.
- Controlled retry policy.

Do not introduce Redis, Kafka or heavyweight distributed infrastructure unnecessarily.

Do not assume the system continues processing while the laptop is switched off.

Prevent duplicate job execution after restart.

---

### 28. Mandatory Security Regression

Preserve the existing Odoo security architecture.

Verify separately:

- Trading Research Viewer.
- Trading Research Analyst.
- Trading Risk Manager.
- Trading System Administrator.

Review whether Risk Manager inheritance of Analyst permissions is justified for each new operation.

Enforce separation for sensitive configuration, approval and risk-control operations.

Test:

- Unauthorized model creation.
- Unauthorized record modification.
- Unauthorized record deletion.
- Cross-company relational references.
- Company switching.
- Forged RPC arguments.
- Direct API calls.
- Unauthorized dashboard data access.
- Unauthorized provider configuration.
- Credential redaction.
- Unauthorized dataset import.
- Unauthorized research execution.
- Immutable historical record protection.
- Virtual ledger manipulation.
- Strategy status manipulation.

Review every new `sudo()` usage.

Use the smallest necessary privilege scope.

Re-execute real-order prohibition source checks.

Extend source checks with outbound endpoint and runtime adapter tests.

Keyword scanning alone is not sufficient to prove that real execution is impossible.

---

### 29. Mandatory P02 Acceptance Criteria

Preserve AC-001 through AC-050 and introduce these additional milestone criteria:

- P02-AC-001: P01 baseline preserved.
- P02-AC-002: Previous defects independently revalidated.
- P02-AC-003: Traceability semantics corrected.
- P02-AC-004: Evidence integrity verified.
- P02-AC-005: Source checkpoint established.
- P02-AC-006: Exchange calendar service implemented.
- P02-AC-007: Session-aware candle validation.
- P02-AC-008: Point-in-time data contract.
- P02-AC-009: Instrument reference mapping integrity.
- P02-AC-010: Data quality eligibility enforcement.
- P02-AC-011: Synthetic-data isolation.
- P02-AC-012: Read-only provider interface.
- P02-AC-013: SmartAPI adapter fixture tests.
- P02-AC-014: Provider timeout and rate-limit protection.
- P02-AC-015: Secure credential handling.
- P02-AC-016: Live verification correctly classified.
- P02-AC-017: Technical indicator mathematical verification.
- P02-AC-018: Indicator prefix invariance.
- P02-AC-019: Versioned research engine contract.
- P02-AC-020: Effective-dated transaction costs.
- P02-AC-021: Fee-aware position sizing.
- P02-AC-022: Independent risk veto.
- P02-AC-023: Versioned strategy framework.
- P02-AC-024: ST-01 research strategy implementation.
- P02-AC-025: Conservative historical simulation.
- P02-AC-026: Backtest reproducibility.
- P02-AC-027: Holdout isolation.
- P02-AC-028: Financial performance provenance.
- P02-AC-029: Structured NO TRADE enforcement.
- P02-AC-030: No actionable real-market recommendation leakage.
- P02-AC-031: Virtual ledger integrity.
- P02-AC-032: Virtual execution idempotency.
- P02-AC-033: Premium OWL dashboard improvements.
- P02-AC-034: Actual database-backed chart values.
- P02-AC-035: Authorized dashboard drill-downs.
- P02-AC-036: Real browser verification.
- P02-AC-037: End-to-end performance measurement.
- P02-AC-038: Resource-bound execution.
- P02-AC-039: Complete security regression.
- P02-AC-040: Updated evidence-backed development report.

Criteria relating to later implementation priorities must remain PARTIAL, BLOCKED or NOT_RUN when not fully established.

Do not mark a criterion PASSED solely because a model, method or interface exists.

---

### 30. Mandatory Test Execution Program

Execute relevant existing and new tests.

#### Test Group A — Baseline Regression

Re-execute all previously available tests.

#### Test Group B — Data Quality and Calendar

Test holidays, special sessions, timezone conversion, gaps, incomplete candles, future observations, duplicate imports, token changes and invalid dataset provenance.

#### Test Group C — Provider Integration

Test fixture authentication, expired sessions, malformed responses, rate limits, timeouts, stale quotes, disconnects, subscription restrictions and credential redaction.

Perform real read-only smoke tests only with explicitly authorized credentials and verified access.

#### Test Group D — Quantitative Mathematics

Test every implemented indicator, formula conventions, missing values, warm-up, edge cases, reference fixtures and prefix invariance.

#### Test Group E — Financial Mathematics

Test brokerage, statutory charge configuration, rounding, slippage, gross/net P&L, fee-aware sizing and reward-to-risk calculations.

#### Test Group F — Strategies and Backtesting

Test qualifying and rejected candidates, temporal correctness, next-observation execution, gap losses, stop-target ambiguity, session closure, reproducibility and holdout isolation.

#### Test Group G — Paper Trading

Where implemented, test cash conservation, reservations, fills, duplicate prevention, insufficient capital, partial failures, independent concurrency and restart recovery.

#### Test Group H — Browser UI

Use a real running Odoo 20 Community instance.

Test desktop and mobile rendering, navigation, filters, pagination, charts, KPI reconciliation, loading states, empty states, failure recovery, stale-data warnings and console errors.

#### Test Group I — Installation and Upgrade

Execute:

- Fresh module installation.
- Same-version upgrade.
- Upgrade from the preserved P01 source baseline.
- Upgrade of a populated P01 test database.
- Data retention checks.
- XML ID retention checks.
- Immutable snapshot retention checks.

Do not test destructive upgrades against the owner's working database.

#### Test Group J — True Concurrency

Use separate committed database transactions, independent connections or processes.

Verify actual overlapping execution.

Cover applicable ingestion, research job, dataset and virtual ledger operations.

A sequential test must not be labeled a concurrency test.

#### Test Group K — Performance and Recovery

Measure resource use and exercise database failure, provider interruption, application restart, interrupted processing and memory-pressure behavior.

---

### 31. Execution Priorities and Definition of Done

Execute in dependency order.

Priority 0:

- Audit.
- Baseline regression.
- Traceability correction.
- Evidence integrity.
- Security preservation.

Priority 1:

- Exchange calendar.
- Reference data.
- Point-in-time data.
- Market data quality.
- Read-only provider foundation.

Priority 2:

- Indicator library.
- Research engine contract.
- Cost engine.
- Independent risk calculations.

Priority 3:

- ST-01.
- Historical backtesting.
- Financial research metrics.
- Validation infrastructure.

Priority 4:

- Initial virtual ledger.
- Background jobs.
- Expanded research capabilities.

Throughout all priorities, implement the associated functional dashboard improvements and tests.

Complete the strongest possible verified vertical slice.

Do not prioritize twenty superficial strategies over one correctly implemented and independently tested strategy.

Do not spend the entire execution generating documentation without meaningful implementation.

Do not spend the entire execution polishing dashboard cosmetics while core research remains broken.

When an external dependency blocks a feature, continue independent development and document the blocker.

---

### 32. Mandatory Updated Documentation

Update:

- `README.md`
- `docs/MASTER_REQUIREMENTS.md` only through clearly identified additions, preserving the original requirements.
- `docs/ARCHITECTURE.md`
- `docs/REQUIREMENTS_TRACEABILITY.md`
- `docs/DEVELOPMENT_PLAN.md`
- `docs/DECISION_LOG.md`
- `docs/RISK_REGISTER.md`

Create where relevant:

- `docs/MARKET_DATA_SOURCES.md`
- `docs/SMARTAPI_SETUP.md`
- `docs/EXCHANGE_CALENDAR.md`
- `docs/INDICATOR_FORMULAS.md`
- `docs/STRATEGY_SPECIFICATIONS.md`
- `docs/TRANSACTION_COST_MODEL.md`
- `docs/RISK_POLICY.md`
- `docs/BACKTEST_EXECUTION_POLICY.md`
- `docs/DASHBOARD_KPI_DEFINITIONS.md`
- `docs/PAPER_LEDGER_INVARIANTS.md`
- `docs/VALIDATION_PROTOCOL.md`

Documentation must describe actual implemented behavior.

Do not document unimplemented functionality as an available user feature.

---

### 33. Mandatory Evidence Artifacts

Create a new milestone evidence directory:

`docs/evidence/p02/`

Recommended subdirectories:

- baseline/
- installation/
- upgrade/
- unit/
- integration/
- provider/
- calendar/
- quantitative/
- financial/
- backtesting/
- paper/
- browser/
- screenshots/
- concurrency/
- performance/
- security/

Store actual evidence.

Capture:

- Exact commands.
- Exit codes.
- Raw sanitized logs.
- Test runner counts.
- Execution durations.
- Environment versions.
- Dataset identities.
- Actual browser screenshots.
- Financial calculation fixtures.
- Reconciliation results.
- Measured performance.
- Concurrency evidence.

Create:

`docs/evidence/p02/manifest.sha256`

Verify the manifest before finalizing.

Do not include private credentials or data whose redistribution is unauthorized.

---

### 34. Mandatory DEVELOPMENT_REPORT.md

At the end of this development run, update the module-root file:

`DEVELOPMENT_REPORT.md`

Preserve the original 22-section report structure required by Master Prompt 01.

Include additional P02-specific sections as necessary.

The updated report must provide:

#### A. Previous Milestone Comparison

- P01 baseline.
- P02 actual results.
- Newly implemented capabilities.
- Preserved capabilities.
- Regressions detected.
- Regressions repaired.
- Remaining blockers.

#### B. Implementation Delta

For each significant change:

- Requirement ID.
- File path.
- Previous behavior.
- New behavior.
- Implementation status.
- Test evidence.
- Remaining limitation.

#### C. Full Requirements Traceability

Report all original requirements and additional P02 requirements.

Preserve stable IDs.

Do not omit unfinished requirements.

#### D. Research Engine Inventory

Report RE-01 through RE-25 individually.

Include implementation status, mathematical method, data requirements, available data, validation evidence and eligibility.

#### E. Strategy Inventory

Report ST-01 through ST-20 individually.

Include implementation version, research status, experiment evidence, cost assumptions and eligibility.

#### F. SmartAPI Integration

Separate:

- Adapter implementation.
- Fixture integration verification.
- Authorized historical data verification.
- Authorized live quote verification.
- WebSocket verification.
- Account entitlement.
- Static IP requirements.
- Remaining owner setup.

Do not report mocked API tests as live integration.

#### G. Financial Research Results

Separate:

- Synthetic correctness tests.
- Historical financial experiments.
- Out-of-sample experiments.
- Walk-forward experiments.
- Prospective paper trading.

Include only actual measured results.

#### H. Dashboard Inventory

Report all nine original dashboard areas.

Include actual implemented KPIs, filters, chart sources, drill-downs, browser evidence and missing functionality.

#### I. Full Test Inventory

Use explicit statuses:

- PASSED.
- FAILED.
- BLOCKED.
- SKIPPED.
- NOT_RUN.

Use separate coverage mappings for grouped requirements.

Do not add grouped references to executed test totals.

#### J. Acceptance Criteria

Report individually:

- AC-001 through AC-050.
- P02-AC-001 through P02-AC-040.

#### K. Business Invariants

Report INV-01 through INV-30 individually.

Distinguish current enforced guards from unimplemented future controls.

#### L. Performance

Include actual measurements with hardware, dataset size, workload type and execution method.

#### M. Completion Metrics

Report:

- Comparable original requirement coverage.
- Functional implementation coverage.
- Acceptance verification coverage.
- Executed test counts.
- Research engine implementation counts.
- Strategy implementation counts.
- Strategy validation counts.
- Dashboard implementation status.

Explain denominators.

Do not inflate progress through optional technology requirements, documentation headings or duplicated assertions.

#### N. Remaining Work and Next Prompt Handoff

Provide:

- Critical blockers.
- High-priority incomplete features.
- Required repairs.
- External dependencies.
- Exact source paths.
- Missing test evidence.
- Performance bottlenecks.
- Recommended next milestone.

The next agent must be able to continue without repeating completed investigation.

---

### 35. Final Readiness Rules

Choose the highest genuinely supported readiness state:

- DEVELOPMENT INCOMPLETE.
- FOUNDATION VERIFIED.
- HISTORICAL RESEARCH READY.
- PAPER TRADING TEST READY.
- VERIFIED RESEARCH BETA.
- VALIDATED RESEARCH RELEASE READY.

Add a specific scope qualification.

A completed indicator library does not prove a profitable trading strategy.

A completed backtest engine does not prove positive expectancy.

Synthetic tests do not prove financial performance.

A passing browser test does not prove dashboard financial correctness.

A working provider adapter does not prove live account access.

Historical profitability does not guarantee future profitability.

Do not claim actionable real-market recommendation readiness during P02.

---

### 36. Final Execution Instruction

Begin actual implementation immediately.

Read the previous report and governing requirements. Inspect existing development. Re-execute the baseline tests. Repair discovered defects. Implement the highest-priority functional components. Build and validate the associated premium native Odoo dashboard features. Execute mathematical, financial, database, security and browser tests.

Continue until the strongest achievable verified milestone is established.

Do not stop merely because a plan has been generated.

Do not fabricate development completion, market data, research results, test results, dashboard values or profitability.

At completion, print:

```text
PROJECT: Golok AI Trading Lab Pro
MILESTONE: P02
PREVIOUS BASELINE:
PREVIOUS REGRESSIONS VERIFIED:
NEW FUNCTIONAL COMPONENTS:
PARTIAL COMPONENTS:
RESEARCH ENGINES IMPLEMENTED:
STRATEGIES IMPLEMENTED:
STRATEGIES FINANCIALLY VALIDATED:
SMARTAPI FIXTURE STATUS:
SMARTAPI LIVE STATUS:
BACKTESTING STATUS:
PAPER TRADING STATUS:
DASHBOARD STATUS:
TESTS EXECUTED:
TESTS PASSED:
TESTS FAILED:
TESTS BLOCKED:
TESTS SKIPPED:
TESTS NOT RUN:
CRITICAL BLOCKERS:
ORIGINAL REQUIREMENTS COVERAGE:
FUNCTIONAL IMPLEMENTATION COVERAGE:
ACCEPTANCE CRITERIA VERIFIED:
CURRENT READINESS:
REAL ORDER EXECUTION: PROHIBITED
DEVELOPMENT REPORT PATH:
EVIDENCE MANIFEST PATH:
NEXT RECOMMENDED MILESTONE:
```

Use only actual verified counts and statuses.

The updated DEVELOPMENT_REPORT.md will be submitted for independent technical review and preparation of Master Development Prompt 03.

Build for correctness, transparent quantitative intelligence, conservative financial simulation, professional usability, evidence integrity and long-term maintainability.

END OF MASTER DEVELOPMENT PROMPT 02.


---

## P03 specification addition

# GOLOK AI TRADING LAB PRO

## MASTER AGENTIC DEVELOPMENT PROMPT 03 — OPERATIONAL MARKET DATA PLATFORM, PROFESSIONAL RESEARCH INTELLIGENCE, MULTI-SESSION VALIDATION, ATOMIC PAPER TRADING AND PREMIUM FINANCIAL TERMINAL

### 1. Engineering Mission

Act as a multidisciplinary senior quantitative research and software engineering team responsible for continuing the actual development of Golok AI Trading Lab Pro.

Apply professional quantitative research discipline, institutional-style validation practices, conservative financial modeling, rigorous software engineering and capital protection principles.

Your responsibilities include:

- Principal Odoo 20 Community architecture.
- Senior Python engineering.
- Quantitative financial research.
- Financial market data engineering.
- Angel One SmartAPI integration.
- Statistical strategy validation.
- Financial risk management.
- PostgreSQL transaction integrity.
- Native OWL 3 frontend development.
- Premium financial terminal UX/UI design.
- Cybersecurity.
- Performance engineering.
- Automated quality assurance.
- Evidence integrity and technical documentation.

Build actual working software.

Do not return only plans, architectural descriptions, pseudocode, empty models or recommendations for future implementation.

Inspect, implement, integrate, execute, test, debug, repair, document and verify.

The objective is to establish a working end-to-end research application rather than accumulating disconnected Python services.

---

### 2. Mandatory Governing Documents

Read the complete contents of:

- `docs/MASTER_REQUIREMENTS.md`
- `DEVELOPMENT_REPORT.md`
- `docs/REQUIREMENTS_TRACEABILITY.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT_PLAN.md`
- `docs/DECISION_LOG.md`
- `docs/RISK_REGISTER.md`
- `docs/history/DEVELOPMENT_REPORT_P01.md`
- `docs/SMARTAPI_SETUP.md`
- `docs/MARKET_DATA_SOURCES.md`
- `docs/EXCHANGE_CALENDAR.md`
- `docs/INDICATOR_FORMULAS.md`
- `docs/BACKTEST_EXECUTION_POLICY.md`
- `docs/TRANSACTION_COST_MODEL.md`
- `docs/RISK_POLICY.md`
- `docs/DASHBOARD_KPI_DEFINITIONS.md`
- `README.md`

Inspect any additional documentation created during P01 and P02.

Where a listed file does not exist, record its absence and determine whether the corresponding requirement remains incomplete.

Preserve all governing requirements, including:

- RE-01 through RE-25.
- ST-01 through ST-20.
- INV-01 through INV-30.
- AC-001 through AC-050.
- P02-AC-001 through P02-AC-040.
- Original S-series requirement identifiers.
- All 796 detailed P02 tracking identifiers.

Do not reset project requirements.

Do not recreate the application from scratch.

Do not remove existing verified functionality.

Introduce stable P03 requirement and acceptance identifiers.

---

### 3. Reported P02 Baseline

Treat the following as reported findings requiring repository-level verification.

| Metric | Reported P02 result |
|---|---|
| Original requirements coverage | 72/1,236 |
| Corrected capability-and-process coverage | 56/1,210 |
| Original acceptance criteria | 14/50 |
| P02 acceptance criteria | 26/40 passed |
| P02 functional milestones | 11/23 passed |
| P02 acceptance criteria partial | 12 |
| P02 acceptance criteria not run | 2 |
| Executed tests | 67 |
| Passed tests | 67 |
| Final failed tests | 0 |
| Blocked tests | 2 |
| Planned groups not run | 8 |
| Research engines | 3 partial, 22 not started |
| Indicator series | 19 |
| Strategy candidates | 1 synthetic-scope implementation |
| Financially validated strategies | 0 |
| Actual historical financial experiments | 0 |
| Prospective paper trading | Not implemented |
| SmartAPI live verification | Blocked |
| Evidence manifest entries | 22 |
| Readiness | FOUNDATION VERIFIED |

P02 preserved 149 original module XML IDs during the populated P01 upgrade.

The existing financial replay consists of nine five-minute synthetic bars, one session, one simulated stop-first trade and hypothetical transaction costs.

Do not interpret this as evidence of profitable trading.

---

### 4. Actual Target Hardware

Previously observed environment:

- Windows NT 10.0.26300.
- Intel Core i5-10210U.
- Four physical CPU cores.
- Eight logical processors.
- Approximately 16 GB RAM.
- Approximately 3.4 GiB available memory during initial inspection.
- Intel UHD integrated graphics.
- No dedicated GPU.
- Python 3.14.6.
- PostgreSQL 18.4.
- Odoo 20 Community.
- Edge browser with Playwright.

Module path:

`C:/PycharmProjects/odoo20/custom_addons/golok_ai_trading_lab_pro`

Verify the current environment before implementation.

Preserve CPU-only operation.

The application must not require:

- Paid AI APIs.
- OpenAI API.
- Claude API.
- Gemini API.
- Local LLMs.
- Ollama.
- GPU acceleration.
- Mandatory cloud services.
- Mandatory paid analytics subscriptions.

Use lightweight numerical libraries only where compatible and demonstrably useful.

Do not modify the owner's production environment or downgrade Python without authorization.

---

### 5. Non-Negotiable Product Boundary

The application remains a research, historical validation, monitoring and paper trading platform.

Real-money trading is strictly outside the current development scope.

Prohibit:

- Real broker order placement.
- Real broker order modification.
- Real broker order cancellation.
- Real-money automatic buying or selling.
- Automatic use of actual account balances.
- Fund transfers.
- Automatic allocation of 25% of real capital.
- Dormant or hidden real-order execution.
- Unauthorized accounting mutations.

Angel One access must be read-only except for required authorized authentication operations.

Paper trading must use isolated virtual funds.

All market recommendations generated during P03 must remain research-only, historical or explicitly simulated.

Do not enable actionable real-money BUY or SELL recommendations during this milestone.

Do not guarantee profitability.

---

### 6. Phase P03-A — Independent Baseline Audit

Before extending functionality, inspect and independently verify the P01/P02 implementation.

Audit these important files:

- `models/lab.py`
- `wizard/lab.py`
- `services/calendar.py`
- `services/market_data.py`
- `services/reference.py`
- `services/smartapi.py`
- `services/research.py`
- `services/indicators.py`
- `services/simulation.py`
- `services/backtest.py`
- `static/src/`
- `security/ir.access.csv`
- `security/groups.xml`
- `views/lab.xml`
- `tests/`
- `scripts/`

Re-execute existing:

- Standalone Python tests.
- Fresh Odoo installation tests.
- Module upgrade tests.
- Populated historical upgrade tests.
- Independent PostgreSQL contention tests.
- Real Edge browser tests.
- Source security checks.
- Synthetic backtest reproduction.

Review previous fixes:

- AUD-001: P01 regression verification.
- AUD-002: Prohibited-operation traceability semantics.
- AUD-003: Research authorization before idempotent return.
- ENV-02: PowerShell subprocess handling and test-port isolation.

Prevent their recurrence.

Do not run destructive tests against the owner's actual Odoo database.

Preserve existing XML IDs, installed data, snapshots and input digests.

---

### 7. Source Checkpoint and Evidence Preservation

The module previously had no Git repository.

Inspect the actual repository and its parent directories.

Create a recoverable P02 source checkpoint before modifying files.

Preserve:

- P01 source archive.
- P01 evidence.
- P02 source checkpoint.
- P02 evidence manifest.
- P02 development report.
- P02 traceability baseline.

Archive the previous report at:

`docs/history/DEVELOPMENT_REPORT_P02.md`

Store new evidence under:

`docs/evidence/p03/`

Verify all referenced P02 artifact hashes against actual local files.

Do not assume a manifest proves test execution merely because its syntax is valid.

Report missing, modified or inconsistent evidence.

Exclude credentials, private datasets, databases, runtime sessions and sensitive broker information from source checkpoints.

---

### 8. Complete Traceability Reconciliation

The P02 report describes substantial new implementations, while numerous original requirement rows still retain P01 statuses.

Correct this inconsistency.

Examples requiring inspection:

- Original EMA, RSI, MACD and VWAP requirement rows.
- Research engine V2 contract requirements.
- Calendar-related requirements.
- SmartAPI authentication and adapter requirements.
- Transaction cost requirements.
- Position sizing requirements.
- Historical replay requirements.
- Original acceptance criteria.
- Business invariant implementation paths.

Do not mark a requirement complete merely because a related service exists.

For every original and P02 requirement, reconcile:

- Actual implementation.
- Current source path.
- Scope of implementation.
- Test identity.
- Executed evidence.
- Missing functionality.
- External dependencies.
- Current acceptance status.

Replace generic evidence references with specific supporting tests wherever possible.

Do not incorrectly classify mandatory PostgreSQL usage as an optional platform requirement. Distinguish optional technology mentions from the mandatory product architecture.

Do not confuse:

- An implemented capability.
- A verified mandatory prohibition.
- A temporary scope guard.
- An optional dependency.
- A partially working implementation.
- A blocked external test.
- A fully validated feature.

Maintain separate status dimensions for implementation, software verification, external integration and financial validation.

Recalculate progress using a documented counting method.

Retain original metrics for historical comparison.

Reconcile the reported 67 test executions against exact runner counts and scripted scenarios. Every counted execution must have a unique execution record.

Do not inflate counts through grouped tests or duplicated references.

---

### 9. Phase P03-B — Persistent Instrument Reference Data

Extend `services/reference.py` into a fully integrated Odoo instrument reference subsystem.

Implement persistent versioned records for:

- Instruments.
- Exchanges.
- Trading segments.
- Trading symbols.
- ISIN identifiers.
- Provider tokens.
- Token validity periods.
- Symbol changes.
- Listing dates.
- Delisting dates.
- Suspension periods.
- Tick sizes.
- Lot sizes.
- Sector classifications.
- Corporate actions.
- Reference data sources.
- Source verification.
- Import revisions.
- Effective dates.

Use stable internal instrument identity independent of mutable trading symbols.

Prevent overlapping effective-dated mappings.

Prevent a recycled provider token from being mapped to the wrong historical instrument.

Implement database-backed constraints and concurrency protection.

Support authorized instrument master import and synchronization.

Preserve the earlier P01/P02 instruments and historical references.

Record unknown values explicitly instead of inventing classifications.

Implement a professional instrument directory with search, filters, archived mappings and mapping history.

---

### 10. Corporate Action and Point-in-Time Integrity

Implement effective-dated support for:

- Stock splits.
- Bonus issues.
- Symbol changes.
- Listing and delisting.
- Suspensions.
- Other relevant price-adjustment events.

Store source references, publication dates, effective dates and adjustment methodology.

Preserve original raw observations.

Maintain distinct adjusted and unadjusted price series.

Prevent an experiment from mixing incompatible adjustment conventions.

Avoid applying corporate action information before its historically available date.

Support point-in-time instrument universe reconstruction.

If a complete historical universe cannot be established, explicitly identify survivorship bias.

Do not claim survivorship-bias-free research without supporting historical membership and delisting evidence.

Test split boundaries, conflicting mappings, revised data, missing corporate actions and late publication.

---

### 11. Exchange Calendar V3

Extend the existing `golok.lab.calendar` implementation.

Support versioned exchange calendars with:

- Regular sessions.
- Market holidays.
- Special sessions.
- Multiple session segments.
- Pre-open periods.
- Closing periods.
- Intraday entry cutoffs.
- Intraday exit cutoffs.
- Early closes.
- Trading interruptions.
- Source provenance.

Consult official NSE and BSE sources when available.

Record verification dates and applicable circular references.

If an authoritative calendar cannot be obtained, distinguish operator-curated calendars from verified calendars.

Prevent research decisions during unsupported sessions.

Handle:

- Session boundaries.
- Truncated interval bars.
- Missing final candles.
- Cross-session gaps.
- Asia/Kolkata and UTC conversion.
- Exchange-specific differences.
- Partial or split sessions.

Preserve legacy calendar compatibility while preventing unverified legacy data from gaining elevated eligibility.

---

### 12. Phase P03-C — Operational SmartAPI Integration

The existing `services/smartapi.py` contains a fixture-verified, three-operation REST allowlist.

It remains outside Odoo and lacks operational ingestion and streaming.

Convert it into an authorized, usable, read-only provider integration.

Verify current official documentation:

- https://smartapi.angelone.in/
- https://smartapi.angelone.in/docs
- https://github.com/angel-one/smartapi-python

Document:

- Authentication requirements.
- Account-specific market data entitlement.
- Static IP requirements.
- Historical data limits.
- REST request limits.
- WebSocket restrictions.
- Supported exchanges.
- Supported instrument types.
- Data storage permissions.
- Redistribution restrictions.
- Relevant provider charges.

Do not invent these values.

Do not bypass provider restrictions.

Do not subscribe to paid services without explicit owner authorization.

Implement an Odoo configuration and diagnostics workflow for:

1. Provider setup.
2. Credential availability checking.
3. Connection diagnostics.
4. Authentication status.
5. Instrument synchronization.
6. Historical data synchronization.
7. Latest quote retrieval.
8. Connection health.
9. Session expiry.
10. Error recovery.

Keep sensitive credentials outside ordinary readable database fields.

Use environment-based secrets or an appropriate protected Windows secret mechanism.

Never expose passwords, API keys, TOTP secrets, access tokens or refresh tokens in reports or browser responses.

The owner must configure credentials locally.

Do not request that credentials be pasted into ChatGPT or development reports.

---

### 13. Safe Authorized Network Transport

Implement a real transport behind the existing narrow adapter.

Enforce:

- Explicit HTTPS destinations.
- Approved endpoint paths.
- Approved HTTP methods.
- TLS verification.
- Request timeouts.
- Response size limits.
- Response schema checks.
- Safe error sanitation.
- Bounded retry policies.
- Exponential backoff.
- Rate-limit handling.
- Redirect restrictions.

Do not allow arbitrary endpoint strings, generic broker method execution or arbitrary outbound URLs through RPC.

Prevent unauthorized server-side requests.

Apply shared provider request limits across workers and processes, rather than relying only on a client-local limiter.

Do not permit real-order endpoints.

The default installation must remain offline-safe.

If authorized credentials or network requirements are unavailable, retain fixture testing and report live integration as BLOCKED.

Continue implementing independent functionality.

---

### 14. Provider-to-ORM Market Data Pipeline

Create a complete ingestion workflow:

Provider response → schema validation → token resolution → calendar validation → timestamp validation → data quality evaluation → provenance recording → atomic persistence → research eligibility.

Implement:

- Historical download jobs.
- Bounded request windows.
- Download checkpoints.
- Retry and recovery.
- Idempotent imports.
- Duplicate response handling.
- Partial response handling.
- Conflicting price handling.
- Provider error classification.
- Dataset quarantine.
- Synchronization history.
- Per-instrument freshness.
- Source authorization metadata.

Preserve:

- Market event time.
- Source publication time.
- Provider receipt time.
- Local ingestion time.
- Candle opening time.
- Candle closing time.

Never substitute receipt time for a missing market timestamp.

Do not silently combine data from incompatible sources.

A user-entered provider name must not prove source authenticity.

Implement an explicit eligibility policy separating:

- Synthetic data.
- Imported unverified data.
- Authorized historical data.
- Delayed data.
- Verified live observations.
- Quarantined data.

Only appropriately authorized and validated data may enter relevant financial research experiments.

---

### 15. WebSocket and Live Market Data Foundation

Implement authorized WebSocket market data support if provider documentation and available environment permit.

Keep networking outside the browser.

Implement a resource-bounded connection manager with:

- Authentication.
- Subscription registry.
- Subscription limits.
- Heartbeat monitoring.
- Reconnection.
- Backoff.
- Sequence validation.
- Out-of-order tick handling.
- Duplicate tick handling.
- Per-instrument freshness.
- Bounded queues.
- Overflow handling.
- Reconnection reconciliation.

Implement candle aggregation only from sufficiently reliable observations.

Mark incomplete bars explicitly.

Never create artificial candles to conceal missing data.

Differentiate connectivity from actual market freshness.

On disconnection:

- Mark affected observations stale.
- Block new simulation entries requiring fresh data.
- Invalidate affected research eligibility.
- Do not generate simulated fills from stale prices.
- Preserve existing positions and historical records.
- Expose the failure prominently.

Run deterministic streaming fixtures and failure simulations.

Perform real WebSocket verification only with authorized access.

If unsupported or blocked, report the precise limitation.

---

### 16. Owner-Friendly SmartAPI Setup Wizard

Build a professional setup experience inside Odoo.

The owner must be able to understand the connection state without reading Python logs.

Provide:

- Setup instructions.
- Provider capability summary.
- Credentials configured indicator.
- Static IP requirement information.
- Authorization status.
- Connection test action.
- Session status.
- Historical data test action.
- Quote retrieval test action.
- Last successful synchronization.
- Sanitized error explanation.
- Next required action.

Use clear statuses:

- NOT CONFIGURED.
- AUTHORIZATION REQUIRED.
- OFFLINE.
- CONNECTING.
- CONNECTED.
- DEGRADED.
- RATE LIMITED.
- STALE.
- BLOCKED.
- ERROR.

Never display CONNECTED solely because credentials are present.

Add authorized server-side permission checks for every setup operation.

Do not expose a generic broker API console.

---

### 17. Phase P03-D — Complete Mathematical Indicator Verification

P02 reports 19 causal indicator series.

Independently verify every original indicator requirement:

- SMA.
- EMA.
- RSI.
- MACD.
- ATR.
- VWAP.
- ADX.
- Bollinger Bands.
- Stochastic Oscillator.
- Relative Volume.
- Rate of Change.
- On-Balance Volume.
- Historical Volatility.
- Rolling Highs and Lows.
- Opening Range.
- Relative Strength.
- Price Gaps.
- Volume Spikes.
- Trend Slopes.

For each indicator, document:

- Exact formula.
- Initialization.
- Smoothing convention.
- Required warm-up.
- Numerical tolerance.
- Session behavior.
- Missing-data behavior.
- Input validity.
- Benchmark dependency.
- Algorithm version.

Expand independent reference tests beyond the existing prefix-invariance fixture.

Use hand-calculated cases and independent reference implementations where possible.

Verify:

- Constant price series.
- Increasing and decreasing prices.
- Price gaps.
- Zero volume.
- Missing observations.
- Invalid numerical values.
- Very short datasets.
- Multiple sessions.
- Different intervals.
- Benchmark alignment.
- Extreme values.
- Prefix invariance.
- Incremental versus full calculation consistency.

Distinguish actual tick-level VWAP from OHLCV-derived approximations.

Do not describe an approximate VWAP as exact exchange VWAP.

---

### 18. Professional Research Engine Framework V3

Replace the current three-engine ORM slice with a versioned, extensible research registry.

Preserve RE-01 through RE-25.

Each engine must declare:

- Engine ID and version.
- Required inputs.
- Optional inputs.
- Applicable strategies.
- Data eligibility requirements.
- Minimum sample size.
- Execution limits.
- Output schema.
- Evidence format.
- Known limitations.

Persist each research result with:

- Company.
- Instrument.
- Dataset identity.
- Dataset digest.
- Research cutoff.
- Calculation version.
- Result state.
- Supporting observations.
- Contradictory observations.
- Missing inputs.
- Warnings.
- Execution duration.

Supported result states:

- COMPLETED.
- NOT_APPLICABLE.
- INSUFFICIENT_DATA.
- STALE_DATA.
- ERROR.

Do not return positive default findings for missing inputs.

Do not convert an engine registry entry into a completed engine count.

---

### 19. Priority OHLCV Research Engines

Complete and integrate the following engines wherever their data prerequisites are satisfied.

**RE-01 — Technical Analysis**

Provide trend, momentum and indicator interpretation rather than a single moving-average value.

**RE-03 — Price Action**

Analyze swing structure, directional movement, candle ranges, higher highs, lower lows and documented structural conditions.

**RE-04 — Candlestick Patterns**

Implement objective mathematical pattern definitions. Do not treat patterns as guaranteed predictive signals.

**RE-05 — Volume Intelligence**

Implement relative volume, unusual volume, session-adjusted baselines and price-volume relationships.

**RE-06 — Support and Resistance**

Use causal rolling or confirmed swing levels. A swing requiring later confirmation must not be treated as known earlier.

**RE-07 — Breakout Detection**

Evaluate previously established levels, breakout timing and confirmation.

**RE-08 — False Breakout Detection**

Identify explicitly defined failed breakout conditions only after supporting observations become available.

**RE-09 — Market Trend**

Distinguish instrument-specific trends from market-wide trends. Require benchmark evidence for market-wide conclusions.

**RE-15 — Historical Patterns**

Evaluate reproducible historical pattern definitions, available samples and outcome uncertainty.

**RE-17 — Liquidity Analysis**

Use authorized spread and depth data when available. Clearly identify OHLCV-based liquidity measurements as proxies.

**RE-18 — Volatility Analysis**

Expand ATR-based research with realized volatility, range analysis and documented volatility classifications.

**RE-19 — Momentum Analysis**

Analyze direction, strength and persistence using documented causal calculations.

**RE-20 — Abnormal Market Activity**

Detect unusual price, volume or volatility behavior. Do not claim that statistical abnormalities prove manipulation.

Prioritize mathematical correctness and Odoo integration.

Implement complete engine-specific tests.

Do not create multiple superficial engines that merely rename the same indicator.

---

### 20. External-Data Research Engines

Create proper data contracts for:

- RE-02 Fundamental Analysis.
- RE-10 Sector Performance.
- RE-11 Benchmark Index Analysis.
- RE-12 Global Market Context.
- RE-13 Financial News and Event Analysis.
- RE-14 Institutional Activity Proxies.

Implement only where lawful, authorized and sufficiently reliable sources exist.

Record publication timestamps.

Fundamental information must be point-in-time.

News information must not be available to a historical decision before publication.

Institutional activity proxies must be labeled as proxies.

Do not invent financial statements, news, sector data, fund flows or institutional order activity.

Do not introduce unauthorized scraping or mandatory paid AI services.

Keep unsupported capabilities explicitly incomplete.

---

### 21. Market Regime Intelligence

Implement a transparent regime classification framework.

Support:

- Bullish trend.
- Bearish trend.
- Range-bound market.
- High volatility.
- Low volatility.
- Strong momentum.
- Weak momentum.
- Abnormal stress.
- Insufficient evidence.

Use independently verified inputs.

Allow trend and volatility classifications to coexist when appropriate.

Do not force incompatible categories into a single arbitrary score.

Distinguish instrument regimes from benchmark and market-wide regimes.

Persist classification versions and evidence.

Prevent strategy selection from ignoring incompatible regimes.

Provide a market-wide research suspension or NO TRADE mechanism for insufficient or unreliable market conditions.

---

### 22. Phase P03-E — Verified Transaction Cost Engine V2

Extend `services/simulation.py`.

Implement persistent, versioned Indian equity tariff configurations.

Support applicable:

- Brokerage.
- Securities Transaction Tax.
- Exchange transaction charges.
- SEBI charges.
- GST.
- Stamp duty.
- Spread.
- Slippage.
- Other verified costs.

Verify applicable rates using authoritative current and historical sources.

Do not use today's tariff schedule for all historical experiments unless clearly justified and labeled.

Store:

- Source.
- Verification date.
- Effective date range.
- Exchange.
- Instrument segment.
- Transaction side.
- Charge basis.
- Percentage or fixed amount.
- Minimum and maximum charge.
- Rounding policy.
- Verification status.

Support correct handling of brokerage caps and applicable order-level versus fill-level charges.

Prevent repeated charging caused by partial fills where inappropriate.

Separate:

- Hypothetical tariffs.
- Estimated tariffs.
- Verified tariffs.

Add a transaction cost calculator accessible through Odoo.

Validate against independently calculated examples and official broker calculators or sanitized contract-note examples when legitimately available.

Do not fabricate reconciliation evidence.

---

### 23. Independent Capital Protection and Portfolio Risk

Expand the existing position-sizing veto into a persistent risk-policy system.

Default virtual reference capital: INR 50,000.

Initial experimental limits:

- Planned per-trade risk: 0.5%.
- Planned daily loss threshold: 1%.
- Maximum daily paper entries: 3.
- Pause after two consecutive losing trades.
- Minimum planned net reward-to-risk ratio: 2:1.
- Preferred ratio: 3:1.
- No leverage.
- No averaging losing positions.
- No martingale.
- Long-only simulation.
- No planned overnight intraday positions.

Treat these as initial configurable simulation policies, not proven optimal settings.

Implement:

- Fee-aware position sizing.
- Capital reservation.
- Aggregate portfolio exposure.
- Existing open-position risk.
- Remaining daily risk budget.
- Sector concentration.
- Correlation risk where evidence is available.
- Maximum concurrent exposure.
- Liquidity restrictions.
- Daily loss monitoring.
- Consecutive-loss monitoring.
- Risk suspension.
- Paper trading kill switch.

Prevent multiple concurrent candidates from independently consuming the same available virtual capital or risk budget.

Recheck risk immediately before simulated execution.

All risk vetoes must be independent of research scores.

A stop loss is not a guaranteed loss limit.

---

### 24. Phase P03-F — Persistent Strategy Registry

Convert the existing ST-01 code-hashed specification into a persistent strategy research framework.

Implement records for:

- Strategy definitions.
- Strategy versions.
- Immutable parameters.
- Required research engines.
- Required datasets.
- Applicable market regimes.
- Code digest.
- Cost policy.
- Risk policy.
- Entry and exit rules.
- Validation status.
- Experiment history.
- Suspension status.
- Approval history.

Use states such as:

- DRAFT.
- RESEARCH_ONLY.
- BACKTESTED.
- VALIDATION_FAILED.
- VALIDATION_BLOCKED.
- PAPER_EVALUATION.
- SUSPENDED.

Strategy approval and promotion must be explicit, authorized and auditable.

Do not automatically promote strategies based on one favorable backtest.

No P03 strategy may become actionable for real-money trading.

---

### 25. Complete ST-01 Opening Range Breakout

Extend ST-01 beyond the existing single-session synthetic fixture.

Implement a complete research lifecycle with:

- Multi-session input.
- Opening range construction.
- Volume confirmation.
- Entry validity.
- Session-specific entry cutoff.
- Stop methodology.
- Target methodology.
- Holding period constraints.
- Fee-aware risk calculation.
- Entry deviation rejection.
- Invalidation.
- Session-end handling.

Recalculate candidate eligibility at the simulated execution time.

Do not fill at an opening price that occurred before the decision became available.

Do not use the full future volume of an entry candle to justify an earlier fill.

Test winning, losing, neutral, rejected and unresolved cases.

Preserve rejected candidates and failed experiments.

---

### 26. Additional Strategy Candidates

After ST-01 and the general framework pass targeted tests, prioritize:

- ST-02: VWAP Pullback.
- ST-03: VWAP Reclaim.
- ST-04: Trend Following.
- ST-05: Momentum Continuation.
- ST-06: Volume Confirmed Breakout.
- ST-08: Mean Reversion.

Implement these as independently testable research candidates where their prerequisites are satisfied.

Use distinct entry and exit logic.

Avoid superficial duplicates.

Every strategy must define:

- Required data.
- Applicable regime.
- Entry conditions.
- Exit conditions.
- Stop policy.
- Target policy.
- Invalidation.
- Risk requirements.
- Validation protocol.

Do not claim profitability merely because a strategy generates simulated trades.

Complete one reliable strategy before expanding to additional candidates.

Preserve all remaining ST identifiers in the development backlog.

---

### 27. Phase P03-G — Multi-Session Historical Backtesting

Extend `services/backtest.py` into a persistent, multi-session backtesting application.

Connect it to Odoo through authorized models, wizards and bounded background jobs.

The owner must be able to:

- Select an eligible dataset.
- Select a strategy version.
- Select a date range.
- Select a virtual starting balance.
- Select a cost model.
- Select a risk policy.
- Configure execution assumptions.
- Run an experiment.
- Inspect results.
- Inspect simulated trades.
- Reproduce the experiment.

Do not leave the only backtesting interface as a standalone CLI.

Use the same quantitative, strategy, cost and risk logic across historical replay and paper simulation.

Implement:

- Chronological event processing.
- Multiple trading sessions.
- Multiple instruments.
- Persistent account state.
- Capital constraints.
- Simulated latency.
- Conservative fills.
- Gap handling.
- Stop and target ambiguity.
- Missing data handling.
- Session-end rules.
- Illiquid instruments.
- Suspended instruments.
- Partial fills where supported.
- Unresolved execution states.

If no valid exit observation exists, do not invent a closing price. Mark the position or experiment unresolved according to the documented execution policy.

Do not discard unresolved or losing trades to improve statistics.

---

### 28. Immutable Experiment Specification

Every experiment must preserve:

- Experiment ID.
- Company.
- Dataset identifiers.
- Dataset digest.
- Universe selection method.
- Calendar revision.
- Corporate action revision.
- Strategy version.
- Code digest.
- Parameter values.
- Indicator version.
- Cost schedule version.
- Risk configuration.
- Execution assumptions.
- Training period.
- Validation period.
- Holdout period.
- Benchmark.
- Random seed where applicable.
- Predeclared acceptance rules.

Freeze these values before execution.

Store append-only results and execution events.

Prevent overwriting completed experiments.

Use new experiment versions for any changed parameters.

Persist all failed and aborted runs with their actual status.

---

### 29. Holdout Isolation and Walk-Forward Validation

P02 has a partition label but no enforced chronological split or one-time holdout isolation.

Implement:

- Chronological training windows.
- Validation windows.
- Final untouched holdout.
- Walk-forward rolling or expanding windows.
- Purging where overlapping outcome windows require it.
- Embargo where appropriate.
- Parameter selection restrictions.
- Experiment lineage.
- Dataset revision tracking.
- Holdout consumption audit.

Prevent the same holdout from being repeatedly reused for parameter optimization.

Prevent indirect leakage through:

- Future-fitted normalization.
- Future universe membership.
- Later corporate action information.
- Future benchmark values.
- Overlapping labels.
- Post-hoc strategy selection.

Record training and evaluation windows separately.

Execute synthetic temporal integrity tests even if actual financial datasets are unavailable.

Mark actual financial validation BLOCKED when authorized data or appropriate cost assumptions are missing.

---

### 30. Professional Financial Research Metrics

Implement independently tested calculations for:

- Total considered candidates.
- Rejected candidates.
- Simulated trades.
- Winning trades.
- Losing trades.
- Neutral trades.
- Gross profit and loss.
- Net profit and loss.
- Total costs.
- Average net trade.
- Win rate.
- Profit factor.
- Net expectancy.
- Maximum drawdown.
- Equity curve.
- Consecutive losses.
- Turnover.
- Maximum adverse excursion.
- Maximum favorable excursion.
- Sharpe ratio where meaningful.
- Sortino ratio where meaningful.
- Confidence intervals where justified.

Define the observation unit used for each statistic.

Distinguish trade-level performance from daily portfolio returns.

Handle empty samples and zero denominators without fabricated values.

Calculate drawdown from correctly ordered equity observations.

Preserve negative results.

Do not select strategies solely by win rate.

A high win rate can coexist with negative expectancy.

---

### 31. Professional Profitability Validation Protocol

Define a predeclared strategy evaluation policy.

Assess:

- Net expectancy after all material costs.
- Drawdown.
- Sample adequacy.
- Outcome uncertainty.
- Performance across market regimes.
- Out-of-sample stability.
- Parameter sensitivity.
- Transaction cost sensitivity.
- Execution latency sensitivity.
- Liquidity sensitivity.
- Performance relative to simple baselines.

Implement stress testing and suitable block-bootstrap methods where sample structure supports them.

Account for correlated trades and multiple strategy testing.

Do not treat hundreds of highly correlated observations as hundreds of independent samples.

Reject strategies with insufficient evidence, excessive sensitivity, unstable results or unacceptable risk.

Do not force any strategy to pass.

If all strategies fail, preserve that result.

Maintain separate classifications:

- SOFTWARE VERIFIED.
- SYNTHETIC CORRECTNESS VERIFIED.
- HISTORICAL EVIDENCE AVAILABLE.
- OUT-OF-SAMPLE VALIDATED.
- PROSPECTIVE PAPER EVIDENCE AVAILABLE.
- FINANCIAL VALIDATION INSUFFICIENT.

A software test passing does not establish financial profitability.

---

### 32. Phase P03-H — Master Decision Engine V3

Implement a centralized decision engine with the previous fourteen mandatory gates:

- G01: Source eligibility.
- G02: Instrument eligibility.
- G03: Trading session validity.
- G04: Candle completeness.
- G05: Market data freshness.
- G06: Research input sufficiency.
- G07: Strategy implementation status.
- G08: Strategy validation status.
- G09: Cost model availability.
- G10: Position sizing.
- G11: Independent risk veto.
- G12: Decision expiry.
- G13: Evidence integrity.
- G14: Research-mode restrictions.

Add explicit checks for:

- Portfolio risk.
- Provider health.
- Market regime compatibility.
- Contradictory evidence.
- Duplicate candidates.
- Strategy suspension.
- Unresolved data quality issues.

Return:

- Gate results.
- Gate reasons.
- Required data.
- Supporting evidence.
- Contradictory evidence.
- Strategy version.
- Dataset identity.
- Decision cutoff.
- Expiry.
- Allowed research mode.

Use permitted states:

- WATCH.
- RESEARCH CANDIDATE.
- HISTORICAL CANDIDATE.
- SIMULATION CANDIDATE.
- NO TRADE.
- INVALIDATED.
- EXPIRED.

Real-money actionable recommendation states must remain disabled.

A high score must never override a hard rejection.

---

### 33. Research Quality and Candidate Ranking

Implement a transparent research quality framework.

Separate:

- Data quality.
- Research completeness.
- Strategy validation strength.
- Market compatibility.
- Execution feasibility.
- Estimated risk.
- Statistical evidence.

Do not double-count correlated indicators as independent evidence.

Provide an explanation of each score contribution.

If a 0–100 score is implemented, clearly distinguish it from a calibrated probability.

Do not assign fabricated 90+ or 95+ scores to make the dashboard appear impressive.

Only rank candidates within their permitted research or simulation mode.

Zero qualified candidates must remain an acceptable result.

---

### 34. Phase P03-I — Atomic Paper Trading Ledger

Implement the previously deferred virtual accounting subsystem.

This is a critical P03 target once its core prerequisites are verified.

Create persistent models for:

- Paper trading account.
- Virtual cash balance.
- Cash reservation.
- Simulated order.
- Simulated fill.
- Open position.
- Closed position.
- Virtual ledger event.
- Trading journal.
- Account equity snapshot.
- Daily risk state.

Keep all balances strictly virtual.

Default configurable virtual starting balance: INR 50,000.

Use exact financial calculations and an explicitly documented rounding policy.

Do not use real broker balances.

Do not create actual Odoo accounting entries.

Implement atomic account and position transitions.

---

### 35. Paper Trading Accounting Invariants

Enforce:

- Virtual cash cannot be spent twice.
- Available cash cannot become negative.
- Reserved cash cannot become negative.
- Reservation release cannot be duplicated.
- Filled quantity cannot exceed authorized quantity.
- Closed quantity cannot exceed open quantity.
- Duplicate fills cannot mutate balances twice.
- Fees cannot be counted twice.
- Every material balance change has an immutable ledger event.
- Realized P&L reconciles with closed position records.
- Equity reconciles with cash and marked position value.
- Failed operations leave no partial committed state.

Define the exact cash, reservation, position and fee accounting equations.

Test them using an independent ledger reconciliation implementation.

Use database constraints and account-level transactional locking.

Test genuine concurrent execution with independent transactions.

Prevent time-of-check/time-of-use capital allocation races.

---

### 36. Paper Trading Lifecycle

Implement controlled virtual execution.

Support:

- Candidate submission.
- Risk validation.
- Capital reservation.
- Simulated pending order.
- Simulated fill.
- Partial fill.
- Stop-loss monitoring.
- Target monitoring.
- Partial profit booking.
- Trailing stop logic.
- Order expiry.
- Position closure.
- Session-end square-off policy.
- Virtual daily P&L.
- Trading journal.

Do not create fills from an observation that occurred before order eligibility.

Do not assume execution merely because a candle touched a level.

Distinguish market observation from simulated execution.

When a feed fails or the laptop sleeps:

- Stop creating new unsupported fills.
- Preserve unresolved positions.
- Reconcile subsequent data where available.
- Record missed observations.
- Do not invent stop-loss execution.
- Do not invent square-off prices.

Separate historical replay accounts from prospective paper accounts.

Historical replay must never contaminate prospective performance statistics.

Prospective operation must remain disabled until its actual provider, data quality and risk prerequisites are verified.

---

### 37. Phase P03-J — Automatic Research Scheduler

Create a lightweight native Odoo-compatible background job framework.

Implement:

- Persistent job identity.
- Company scope.
- Job type.
- Requested time.
- Scheduled time.
- Job state.
- Worker ownership.
- Lease or heartbeat.
- Retry count.
- Cancellation state.
- Checkpoint.
- Execution duration.
- Sanitized failure details.

Support:

- Instrument synchronization.
- Historical data synchronization.
- Research execution.
- Backtesting.
- Paper monitoring.
- Data quality maintenance.
- Daily report generation.

Use exchange-aware scheduling.

Apply Asia/Kolkata market session semantics.

Prevent duplicate execution across workers.

Implement database-backed locking and restart recovery.

Use bounded execution and resource controls.

Do not assume work continues when the laptop is powered off.

After startup, identify interrupted jobs and missed research cycles.

Do not backdate missed prospective observations.

---

### 38. Daily Stock Research Workflow

Build the functional orchestration path:

1. Check system resources.
2. Check provider authorization.
3. Check exchange session.
4. Resolve eligible instruments.
5. Synchronize required observations.
6. Validate data freshness and completeness.
7. Calculate required features.
8. Execute applicable research engines.
9. Evaluate market regime.
10. Evaluate strategy candidates.
11. Apply cost calculations.
12. Apply risk gates.
13. Record decision results.
14. Rank eligible research candidates.
15. Persist all accepted and rejected candidates.
16. Update the dashboard.
17. Generate a research report.

The scan must operate over a configurable eligible universe.

Start with a small measured universe rather than assuming 1,000 instruments can be processed in real time.

Do not force a daily tip count.

Support a complete NO TRADE outcome.

Keep real-market actionable outputs disabled.

---

### 39. Phase P03-K — Premium Native OWL Financial Trading Terminal

Upgrade the existing overview into a coherent, professional financial research workspace.

Use verified native Odoo 20 and OWL 3 implementation patterns.

The dashboard is a mandatory working product feature.

Do not create static decorative mockups.

Use actual database-backed metrics.

#### Design language

- Professional financial terminal appearance.
- Compact navigation.
- Clean typography.
- Premium Golok Technology branding.
- Consistent spacing.
- Responsive layouts.
- Accessible controls.
- Clear data provenance.
- Meaningful status colors.
- Light and dark compatibility where supported.
- Efficient local chart assets.
- No mandatory external CDN.
- No oversized decorative cards.
- No fake prices or P&L.

Provide a coherent navigation hierarchy.

Keep the system usable on the target laptop.

---

### 40. Dashboard A — Market Command Center

Implement a unified market overview with:

- Current exchange session.
- Research mode.
- Data provider state.
- Last verified update.
- Eligible instrument population.
- Data quality status.
- Research coverage.
- Latest research run.
- Available authorized benchmark observations.
- Market breadth where available.
- Sector performance where available.
- Market regime where supported.

Show unavailable values explicitly.

Do not display fake Nifty or Bank Nifty prices.

Display a permanent research/simulation-only notice.

---

### 41. Dashboard B — Professional Stock Scanner

Implement an actual research scanner screen.

Provide:

- Search.
- Exchange filter.
- Sector filter where supported.
- Instrument eligibility filter.
- Data quality filter.
- Timeframe filter.
- Strategy filter.
- Research status filter.
- Candidate status filter.
- Pagination.
- Server-side sorting.

Display:

- Instrument.
- Last observed price and timestamp.
- Data freshness.
- Research status.
- Applicable engines.
- Market regime.
- Candidate status.
- Risk rejection reason.
- Research duration.
- Last scan time.

Provide a controlled Run Research action with persistent job status.

Do not execute heavyweight research directly inside a long browser RPC.

---

### 42. Dashboard C — Research Opportunities

Display actual generated historical or simulated candidates.

Include:

- Instrument.
- Strategy.
- Candidate type.
- Research score if justified.
- Hypothetical entry.
- Hypothetical stop.
- Hypothetical target.
- Virtual quantity.
- Estimated transaction costs.
- Estimated planned downside.
- Estimated net reward.
- Reward-to-risk.
- Candidate validity.
- Supporting evidence.
- Contradictory evidence.
- Gate outcomes.

Clearly distinguish research candidates from actionable real-money instructions.

Do not display a real-market BUY button.

A rejected or empty opportunity list is a valid outcome.

---

### 43. Dashboard D — Advanced Stock Research Terminal

Expand the existing latest-snapshot chart.

Implement:

- Instrument selection.
- Timeframe selection.
- Date range selection.
- Candlestick chart.
- Volume chart.
- SMA and EMA overlays.
- VWAP overlay where valid.
- Opening range visualization.
- Support and resistance observations.
- Indicator panel.
- Research engine results.
- Dataset provenance.
- Historical cutoff.
- Calendar revision.
- Data quality warning.
- Strategy analysis.

Use bounded server-side chart retrieval.

Do not silently truncate data without identifying displayed coverage.

Preserve candle chronology.

Allow authorized drill-down to source observations and research snapshots.

Keep the existing 60-row chart behavior compatible where applicable, while introducing documented bounded historical navigation.

---

### 44. Dashboard E — Paper Trading Portfolio

Where the ledger is actually implemented, display:

- Initial virtual capital.
- Available virtual cash.
- Reserved cash.
- Open positions.
- Closed positions.
- Realized virtual P&L.
- Unrealized virtual P&L.
- Virtual equity.
- Daily virtual return.
- Total trading costs.
- Equity curve.
- Drawdown curve.
- Trading journal.

Clearly identify historical replay versus prospective paper trading.

Display data freshness for open-position marks.

Do not represent stale marks as live equity.

Every dashboard value must reconcile with the underlying virtual ledger.

---

### 45. Dashboard F — Strategy Intelligence Laboratory

Implement:

- Strategy registry.
- Version history.
- Experiment launch workflow.
- Experiment queue.
- Backtest results.
- Simulated trade drill-down.
- Cost breakdown.
- Net expectancy.
- Sample size.
- Drawdown.
- Validation partition comparison.
- Walk-forward results where available.
- Benchmark comparison.
- Validation state.
- Rejected experiment history.

Never hide failed strategies.

Display synthetic and actual historical experiments separately.

Use NOT TESTED or BLOCKED where appropriate.

---

### 46. Dashboard G — Risk Control Center

Display:

- Virtual reference capital.
- Per-trade planned risk budget.
- Daily loss threshold.
- Remaining planned risk budget.
- Capital exposure.
- Reserved cash.
- Consecutive losses.
- Open-position exposure.
- Sector concentration where available.
- Strategy suspensions.
- Risk rejection history.
- Paper trading kill switch state.

Protect sensitive risk policy changes using server-side authorization.

The kill switch must stop new virtual exposure without deleting historical records or pretending open positions have been closed.

---

### 47. Dashboard H — Provider and System Health

Display:

- SmartAPI configuration state.
- Authorization state.
- REST health.
- WebSocket state where implemented.
- Session expiry.
- Request budget.
- Synchronization history.
- Per-instrument data freshness.
- Job queue.
- Failed jobs.
- CPU usage.
- Memory usage.
- Available system memory.
- Research duration.
- Database workload metrics where available.

Provide clear remediation guidance.

Do not expose secret values or unrestricted internal diagnostics.

---

### 48. Dashboard I — Daily Research Report

Implement a persistent daily report with:

- Trading session date.
- Market data coverage.
- Instruments scanned.
- Research engines executed.
- Candidate count.
- Rejected candidate count.
- Rejection reasons.
- Research limitations.
- Market regime information.
- Virtual trading performance where available.
- Data provider issues.
- Strategy warnings.
- Risk suspensions.
- Next eligible research cycle.

Use the actual completed job and research records.

Support authorized historical report access.

Do not fabricate a report for a missed or unexecuted research cycle.

---

### 49. Dashboard Readiness Center

Create a dedicated readiness matrix showing:

- Market data foundation.
- Provider integration.
- Live authorization.
- Instrument mapping.
- Data quality.
- Research engines.
- Indicator verification.
- Strategy framework.
- Cost verification.
- Historical validation.
- Holdout isolation.
- Paper ledger.
- Scheduler.
- Security.
- Browser verification.
- Performance.

Every status must be derived from actual operational records or a clearly identified verification artifact.

Do not create a fake overall progress score.

Provide a visible explanation of why real-market actionable recommendations remain disabled.

---

### 50. Phase P03-L — Performance Optimization

The P02 benchmark measured:

- 50 instruments.
- 75 candles per instrument.
- 3,750 rows.
- 361 SQL statements.
- 5.247 seconds total wall time.
- 2.451 seconds ingestion.
- 1.354 seconds research.
- 3.97 milliseconds active-company count query.
- 138.4 MiB sampled Odoo shell peak RSS.

Use this as a historical baseline, not proof of complete system capacity.

Measure new workloads at:

- 50 instruments.
- 100 instruments.
- 250 instruments.
- 500 instruments where safe.

Attempt 1,000 instruments only if earlier results and resource limits justify it.

Measure:

- Actual Odoo process memory.
- PostgreSQL memory where practical.
- Browser responsiveness.
- Available system memory.
- CPU usage.
- Ingestion duration.
- Research duration.
- Query counts.
- Job duration.
- Provider request limits.
- UI latency.

Use bounded reads, batch persistence, appropriate indexes and incremental computations.

Avoid unbounded ORM searches.

Avoid per-candle database writes where safe bulk processing is possible.

Set configurable memory and runtime limits.

Pause or reduce workloads under memory pressure.

Do not claim real-time scanning capacity unless measured under realistic data acquisition and processing conditions.

---

### 51. Comprehensive Security Regression

Preserve Odoo security groups:

- Trading Research Viewer.
- Trading Research Analyst.
- Trading Risk Manager.
- Trading System Administrator.

Verify the role inheritance model.

Enforce sensitive operations through server-side authorization.

Test:

- Unauthorized provider setup.
- Unauthorized credential access.
- Forged RPC arguments.
- Arbitrary endpoint attempts.
- Cross-company dataset access.
- Cross-company instrument references.
- Cross-company paper account access.
- Unauthorized risk changes.
- Unauthorized strategy promotion.
- Unauthorized experiment alteration.
- Unauthorized ledger manipulation.
- Unauthorized job execution.
- Immutable snapshot modification.
- Secret leakage.
- Invalid external redirects.
- Malformed market data.
- Excessive request sizes.

Review every `sudo()` and raw SQL operation.

Prevent privilege escalation through idempotent return paths.

Revalidate real-order prohibition at source, adapter and runtime levels.

Do not rely solely on keyword scanning.

---

### 52. Mandatory P03 Acceptance Criteria

Preserve all earlier acceptance criteria and add:

| ID | Acceptance criterion |
|---|---|
| P03-AC-001 | P01 and P02 source preservation |
| P03-AC-002 | Previous test regression executed |
| P03-AC-003 | Evidence manifests verified |
| P03-AC-004 | Original traceability reconciled |
| P03-AC-005 | Execution counts independently reconciled |
| P03-AC-006 | Persistent instrument mapping |
| P03-AC-007 | Effective-date overlap prevention |
| P03-AC-008 | Corporate action provenance |
| P03-AC-009 | Point-in-time universe integrity |
| P03-AC-010 | Expanded exchange calendar |
| P03-AC-011 | Secure operational provider configuration |
| P03-AC-012 | Real read-only transport implementation |
| P03-AC-013 | Provider-to-ORM ingestion |
| P03-AC-014 | Shared provider rate limiting |
| P03-AC-015 | Historical integration verification |
| P03-AC-016 | Live quote verification |
| P03-AC-017 | Streaming integration verification |
| P03-AC-018 | Provider failure recovery |
| P03-AC-019 | Market data freshness enforcement |
| P03-AC-020 | Complete indicator reference tests |
| P03-AC-021 | Versioned research registry |
| P03-AC-022 | OHLCV-supported research engines |
| P03-AC-023 | Research evidence persistence |
| P03-AC-024 | Market regime classification |
| P03-AC-025 | Persistent tariff configuration |
| P03-AC-026 | Verified tariff provenance |
| P03-AC-027 | Fee-aware risk calculation |
| P03-AC-028 | Aggregate portfolio risk enforcement |
| P03-AC-029 | Persistent strategy registry |
| P03-AC-030 | Multi-session ST-01 |
| P03-AC-031 | Odoo backtesting workflow |
| P03-AC-032 | Immutable experiment specification |
| P03-AC-033 | Multi-instrument historical replay |
| P03-AC-034 | Conservative execution verification |
| P03-AC-035 | Financial metrics correctness |
| P03-AC-036 | Holdout isolation |
| P03-AC-037 | Walk-forward infrastructure |
| P03-AC-038 | Financial validation provenance |
| P03-AC-039 | Master decision gate enforcement |
| P03-AC-040 | Research scoring transparency |
| P03-AC-041 | Atomic virtual cash ledger |
| P03-AC-042 | Reservation reconciliation |
| P03-AC-043 | Virtual position integrity |
| P03-AC-044 | Fill idempotency |
| P03-AC-045 | Paper lifecycle verification |
| P03-AC-046 | Virtual ledger concurrency |
| P03-AC-047 | Paper restart recovery |
| P03-AC-048 | Historical/prospective separation |
| P03-AC-049 | Persistent background jobs |
| P03-AC-050 | Scheduler concurrency protection |
| P03-AC-051 | Daily research orchestration |
| P03-AC-052 | Functional stock scanner |
| P03-AC-053 | Advanced stock research terminal |
| P03-AC-054 | Strategy dashboard |
| P03-AC-055 | Paper portfolio dashboard |
| P03-AC-056 | Risk control dashboard |
| P03-AC-057 | Provider health dashboard |
| P03-AC-058 | Daily research report |
| P03-AC-059 | Dashboard KPI reconciliation |
| P03-AC-060 | Real browser verification |
| P03-AC-061 | End-to-end performance |
| P03-AC-062 | Resource pressure handling |
| P03-AC-063 | Security regression |
| P03-AC-064 | Company isolation |
| P03-AC-065 | No real-order execution |
| P03-AC-066 | No actionable real-market leakage |
| P03-AC-067 | Fresh installation |
| P03-AC-068 | Populated P02 upgrade |
| P03-AC-069 | Complete owner documentation |
| P03-AC-070 | Evidence-backed development handoff |

Do not mark any criterion PASSED without actual supporting execution evidence.

Use PARTIAL when only a restricted slice is verified.

---

### 53. Mandatory Testing Program

Execute the following test groups according to actual implementation.

**A. Baseline regression**

Re-execute all applicable P01 and P02 tests.

**B. Reference data**

Test effective dates, token reuse, duplicate imports, invalid references, corporate actions and concurrency.

**C. Calendar**

Test holidays, special sessions, split sessions, truncated intervals, missing observations and timezone handling.

**D. SmartAPI**

Test authentication fixtures, expired sessions, rate limits, timeouts, malformed responses, unauthorized endpoints and streaming recovery.

Perform actual authorized external tests separately.

**E. Quantitative mathematics**

Test every indicator, formula, boundary, numerical tolerance, warm-up and temporal property.

**F. Research engines**

Test each implemented engine independently and through Odoo integration.

**G. Financial mathematics**

Test tariff selection, charges, fee rounding, position sizing, costs, net P&L and risk calculations.

**H. Backtesting**

Test multiple instruments, multiple sessions, losing strategies, ambiguous fills, missing data, gaps, reproducibility and invalid configurations.

**I. Statistical validation**

Test chronological partitioning, holdout access restrictions, leakage detection and walk-forward windows.

**J. Paper trading**

Test ledger reconciliation, reservations, fills, partial closes, stop/target handling, insufficient cash and restart recovery.

**K. True concurrency**

Use independent committed database transactions or processes for overlapping operations.

Cover ingestion, mapping updates, job claims, virtual reservations, fills and position closure.

**L. Browser UI**

Run real Edge or another supported browser against actual Odoo 20.

Verify every implemented dashboard, navigation, filters, charts, loading states, empty states, error states and authorized drill-downs.

Capture desktop and mobile screenshots.

**M. Installation and migration**

Test fresh installation, same-version upgrade and upgrade from a populated preserved P02 database.

Verify historical records, XML IDs, security rules and immutable digests.

**N. Performance and failure recovery**

Measure actual resource use and exercise interruptions, provider failures, database failures and memory pressure.

**O. Security**

Verify access controls, secret protection, endpoint restrictions and real-order prohibition.

Record exact commands and actual results.

---

### 54. Execution Order and Completion Gates

Execute in the following priority order.

**Priority 0 — Audit and preservation**

Complete baseline verification, evidence preservation and traceability reconciliation.

**Priority 1 — Operational market data**

Complete persistent instrument reference data, calendar improvements, provider setup, ingestion and data eligibility.

**Priority 2 — Research intelligence**

Complete indicator verification, integrated research engines, market regime and persistent research evidence.

**Priority 3 — Financial research**

Complete cost modeling, risk management, strategy persistence, multi-session backtesting and validation infrastructure.

**Priority 4 — Virtual accounting**

Complete the paper ledger, virtual risk enforcement, execution lifecycle and reconciliation tests.

**Priority 5 — Operational orchestration**

Complete persistent jobs, automatic research scheduling and daily research workflow.

**Priority 6 — Premium dashboard**

Implement corresponding functional dashboard screens throughout the previous phases, then consolidate navigation, design consistency and browser verification.

**Priority 7 — Expanded research**

Implement additional strategies and external-data research engines only after the prerequisite vertical slices are stable.

External authorization blockers must not prevent completion of unrelated local functionality.

Do not spend the entire run repeating documentation work.

Do not stop after implementing disconnected services.

Prioritize actual end-to-end user workflows.

If the execution budget is exhausted, leave the application stable and testable and document the exact next action.

---

### 55. Required New and Updated Documentation

Update the governing documentation.

Create or update:

- `docs/SMARTAPI_SETUP.md`
- `docs/OWNER_QUICK_START.md`
- `docs/MARKET_DATA_SOURCES.md`
- `docs/PROVIDER_OPERATIONS.md`
- `docs/REFERENCE_DATA_MODEL.md`
- `docs/CORPORATE_ACTION_POLICY.md`
- `docs/EXCHANGE_CALENDAR.md`
- `docs/INDICATOR_FORMULAS.md`
- `docs/RESEARCH_ENGINE_CATALOG.md`
- `docs/STRATEGY_SPECIFICATIONS.md`
- `docs/TRANSACTION_COST_MODEL.md`
- `docs/RISK_POLICY.md`
- `docs/BACKTEST_EXECUTION_POLICY.md`
- `docs/VALIDATION_PROTOCOL.md`
- `docs/PAPER_LEDGER_INVARIANTS.md`
- `docs/BACKGROUND_JOBS.md`
- `docs/DASHBOARD_KPI_DEFINITIONS.md`
- `docs/SECURITY_MODEL.md`
- `docs/PERFORMANCE_LIMITS.md`

Documentation must reflect actual implemented behavior.

Clearly distinguish current functionality from planned functionality.

Provide simple practical setup instructions suitable for a non-quantitative owner.

---

### 56. Mandatory Evidence Artifacts

Create:

`docs/evidence/p03/`

Organize evidence into:

- baseline/
- installation/
- upgrade/
- unit/
- integration/
- provider/
- calendar/
- reference/
- quantitative/
- financial/
- backtesting/
- validation/
- paper/
- scheduler/
- browser/
- screenshots/
- concurrency/
- performance/
- security/

Capture:

- Exact test commands.
- Exit codes.
- Individual test results.
- Execution counts.
- Execution durations.
- Sanitized logs.
- Environment metadata.
- Source revisions or hashes.
- Dataset metadata.
- Experiment fingerprints.
- Ledger reconciliation results.
- Browser screenshots.
- Actual performance measurements.
- Independent concurrency evidence.

Create:

`docs/evidence/p03/manifest.sha256`

Verify every listed artifact.

Use relative paths.

Record missing evidence explicitly.

Never include broker credentials, session tokens, private account identifiers or unauthorized market data.

---

### 57. Mandatory Review Handoff Package

At the end of P03, create a sanitized review package:

`P03_REVIEW_HANDOFF.zip`

Include:

- `DEVELOPMENT_REPORT.md`
- `docs/REQUIREMENTS_TRACEABILITY.md`
- P03 evidence manifest.
- Exact test command inventory.
- Sanitized execution logs.
- Browser screenshots.
- Acceptance criteria results.
- Business invariant results.
- Research engine inventory.
- Strategy inventory.
- Performance evidence.
- Financial simulation evidence where redistribution is permitted.
- Source file manifest.
- Important implementation diffs or sanitized source files.
- Outstanding blockers.

Exclude:

- API keys.
- Passwords.
- TOTP secrets.
- Broker tokens.
- Private user account information.
- Production database contents.
- Virtual environments.
- Unauthorized historical datasets.
- Sensitive runtime files.

Create a SHA-256 checksum for the ZIP.

The purpose is to allow independent technical review using actual artifacts rather than relying only on the development report.

Do not package the entire development environment.

---

### 58. Mandatory DEVELOPMENT_REPORT.md

Update the module-root report:

`golok_ai_trading_lab_pro/DEVELOPMENT_REPORT.md`

Preserve the original 22-section report structure.

Add detailed P03 information.

#### Executive summary

Include current milestone, verified scope, achieved functionality and critical blockers.

#### Previous milestone comparison

Compare P01, P02 and P03 using comparable metrics.

#### Implementation delta

For every important change include:

- Requirement ID.
- File path.
- Previous behavior.
- New behavior.
- Implementation state.
- Test result.
- Evidence path.
- Remaining limitation.

#### Research engine inventory

Report RE-01 through RE-25 individually.

Distinguish engine registration, algorithm implementation, ORM integration, mathematical verification and financial validation.

#### Strategy inventory

Report ST-01 through ST-20 individually.

Include strategy version, implementation state, data availability, experiment evidence and eligibility.

#### SmartAPI verification

Separate:

- Fixture verification.
- Real transport implementation.
- Actual authorization.
- Historical retrieval.
- Live quotes.
- WebSocket access.
- Operational ingestion.
- Remaining owner setup.

#### Financial research evidence

Separate:

- Synthetic correctness.
- Actual historical experiments.
- Out-of-sample validation.
- Walk-forward evaluation.
- Prospective paper evaluation.

Never mix them into one performance figure.

#### Virtual accounting

Report:

- Virtual cash reconciliation.
- Reservation integrity.
- Position integrity.
- Fill idempotency.
- Concurrent operations.
- Restart recovery.
- Remaining limitations.

#### Dashboard inventory

Report all nine original dashboard areas and the readiness center.

Include actual KPIs, data sources, working controls, screenshots, browser evidence and incomplete behavior.

#### Test inventory

Report individually identifiable executions.

Include exact commands, actual outcomes, durations, evidence paths and failure repairs.

#### Acceptance criteria

Report:

- AC-001 through AC-050.
- P02-AC-001 through P02-AC-040.
- P03-AC-001 through P03-AC-070.

#### Business invariants

Report INV-01 through INV-30 individually.

#### Completion metrics

Report separately:

- Original requirement coverage.
- Corrected functional coverage.
- Constraint compliance.
- P02 acceptance coverage.
- P03 acceptance coverage.
- Research engine implementation.
- Research engine verification.
- Strategy implementation.
- Financial strategy validation.
- Dashboard implementation.
- External integration.
- Virtual accounting.
- Scheduler.
- Test execution.

Disclose denominators and counting methods.

#### Remaining work

Identify all incomplete requirements, dependencies, source paths, missing tests and recommended next implementation.

Do not hide incomplete work.

---

### 59. Final Readiness Assessment

Select the highest actually supported readiness state:

- DEVELOPMENT INCOMPLETE.
- FOUNDATION VERIFIED.
- HISTORICAL RESEARCH READY.
- PAPER TRADING TEST READY.
- VERIFIED RESEARCH BETA.
- VALIDATED RESEARCH RELEASE READY.

Scope the decision carefully.

A working SmartAPI fixture adapter is not a verified live connection.

A synthetic replay is not a financially validated strategy.

A functional paper ledger does not establish future profitability.

A favorable backtest is not a guarantee of future results.

If actual authorized historical validation or prospective paper evidence is missing, say so explicitly.

Do not declare actionable real-market recommendation readiness during P03.

---

### 60. Final Agentic Execution Instruction

Begin actual implementation immediately.

Inspect and preserve the P02 baseline.

Reconcile the traceability matrix.

Build persistent and operational market data workflows.

Connect quantitative services to Odoo.

Expand actual research capabilities.

Implement realistic multi-session experiments.

Establish holdout isolation.

Develop and verify virtual accounting.

Build persistent research jobs.

Create the premium financial research dashboard.

Execute tests.

Repair defects.

Re-execute affected regression tests.

Record actual evidence.

Create the updated DEVELOPMENT_REPORT.md and sanitized P03_REVIEW_HANDOFF.zip.

Do not finish with only a plan.

Do not fabricate results.

At completion, print the following terminal summary using actual measured counts:

```
PROJECT: Golok AI Trading Lab Pro
MILESTONE: P03

P01/P02 BASELINE PRESERVED:
BASELINE REGRESSION:
TRACEABILITY RECONCILED:

NEW FUNCTIONAL COMPONENTS:
PARTIAL COMPONENTS:
REMAINING CRITICAL BLOCKERS:

SMARTAPI FIXTURE STATUS:
SMARTAPI REAL TRANSPORT STATUS:
SMARTAPI HISTORICAL STATUS:
SMARTAPI LIVE QUOTE STATUS:
SMARTAPI WEBSOCKET STATUS:

INDICATORS IMPLEMENTED:
INDICATORS INDEPENDENTLY VERIFIED:

RESEARCH ENGINES IMPLEMENTED:
RESEARCH ENGINES VERIFIED:
STRATEGIES IMPLEMENTED:
STRATEGIES FINANCIALLY VALIDATED:

BACKTESTING STATUS:
HOLDOUT ISOLATION STATUS:
WALK-FORWARD STATUS:

PAPER LEDGER STATUS:
PAPER LIFECYCLE STATUS:
PROSPECTIVE PAPER STATUS:

AUTOMATIC RESEARCH STATUS:
DASHBOARD STATUS:

TESTS EXECUTED:
TESTS PASSED:
TESTS FAILED:
TESTS BLOCKED:
TESTS SKIPPED:
TEST GROUPS NOT RUN:

ORIGINAL REQUIREMENTS COVERAGE:
CORRECTED FUNCTIONAL COVERAGE:
ORIGINAL ACCEPTANCE CRITERIA:
P02 ACCEPTANCE CRITERIA:
P03 ACCEPTANCE CRITERIA:

CPU AND MEMORY RESULTS:
CURRENT READINESS:
REAL ORDER EXECUTION: PROHIBITED
ACTIONABLE REAL-MARKET RECOMMENDATIONS: DISABLED

DEVELOPMENT REPORT PATH:
EVIDENCE MANIFEST PATH:
REVIEW HANDOFF ZIP PATH:
REVIEW HANDOFF SHA-256:

NEXT RECOMMENDED MILESTONE:
```

Build a trustworthy professional quantitative research platform.

Prioritize mathematical correctness, authorized market data, realistic financial simulations, independent risk protection, premium usability and evidence-backed engineering.

END OF MASTER DEVELOPMENT PROMPT 03.
