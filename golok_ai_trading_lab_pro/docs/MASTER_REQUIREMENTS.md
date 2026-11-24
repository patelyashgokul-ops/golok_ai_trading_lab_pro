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

END OF MASTER DEVELOPMENT PROMPT 01.\n\n---\n\n## P02 specification addition\n\n# GOLOK AI TRADING LAB PRO

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
