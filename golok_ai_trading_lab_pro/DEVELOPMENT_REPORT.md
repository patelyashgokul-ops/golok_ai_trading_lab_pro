# Golok AI Trading Lab Pro — P02 development report

## 01 — Executive summary

Development run on 24 November 2026, Asia/Kolkata. P02 reached **FOUNDATION VERIFIED** for calendar-aware descriptive research, a read-only SmartAPI fixture adapter, and fee-aware synthetic replay. P01 reported 72/1,236 original rows and 14/50 acceptance criteria. Reverification used an identical archived source checkpoint, fresh databases and a populated P01 clone. The clone retained all 149 original module XML IDs along with its instruments, datasets, candles and snapshot digests.

New results cover explicit session validation and source publication times, 19 causal indicator series, a cost-aware long-only opening-range research candidate and native historical charts. Real-market validation, prospective paper execution and live recommendation eligibility remain open. The application only emits historical NO TRADE records.

## 02 — Actual environment

Verified Windows NT 10.0.26300, Intel Core i5-10210U, four physical and eight logical cores, 16,918,601,728 bytes total RAM and 3,639,160,832 bytes available at initial reinspection. Intel UHD was the previously identified integrated controller. P02 workloads used CPU. Verified Python 3.14.6, PostgreSQL 18.4, Odoo 20 Community and Edge via Playwright. The module resides in `C:/PycharmProjects/odoo20/custom_addons/golok_ai_trading_lab_pro`. Neither the module nor its immediate add-on parent had a Git repository. The add-on uses native Odoo web and the standard library. Benchmark tooling uses the existing psutil installation. The harness used disposable localhost PostgreSQL databases and disabled demo data without changing the owner's database or dependencies.

## 03 — Architecture implemented

P01's Odoo roles, import wizard, XML IDs, candles and snapshots remain compatible. The new `golok.lab.calendar` ties dates and continuous session boundaries to one immutable venue/company revision. Calendar-bound observations add opening and publication timestamps in UTC. The chart RPC reads company-scoped history, checks the saved input hash, and returns at most 60 rows. Legacy data uses the earlier observation-close semantics.

`services/reference.py` separates effective-dated instrument identity from reused broker tokens. `services/smartapi.py` puts REST calls behind a three-operation allowlist and holds session credentials in memory. `services/indicators.py` implements bounded causal calculations. `services/simulation.py` and `services/backtest.py` implement hypothetical tariffs, an independent risk veto and synthetic replay outside the Odoo ORM. The browser never invokes the provider or backtest service. [Architecture](docs/ARCHITECTURE.md)

## 04 — Files created and modified

| Requirement | File | Previous behavior | P02 behavior and boundary |
|---|---|---|---|
| P02-AC-001–005 | `docs/history/`, `scripts/verify_p01_upgrade.ps1` | In-place documentation and no Git | SHA-verified source ZIP, archived report and populated clone retained |
| P02-AC-006–011 | `services/calendar.py`, `services/market_data.py`, `models/lab.py`, `wizard/lab.py`, `security/ir.access.csv`, `views/lab.xml` | Close-only CSV | Calendar grid, publication times, quarantine and digest-checked replay. Split sessions and source attestation pending. |
| P02-AC-009 | `services/reference.py` | Static instrument records | Rejects overlapping effective dates and resolves recycled tokens in a supplied directory. Persistence pending. |
| P02-AC-012–016 | `services/smartapi.py` | Absent | Fixture-verified REST allowlist, timeouts and sanitized errors. Workstation authorization pending. |
| P02-AC-017–019 | `services/indicators.py`, `models/lab.py` | Three descriptive indicators | 19 time series with version 2 output for three ORM research engines |
| P02-AC-020–030 | `services/simulation.py`, `services/backtest.py`, `scripts/run_backtest.py` | No replay or costs | Fee/risk-aware synthetic ST-01, strategy/input digests and conservative exits |
| P02-AC-033–036 | `static/src/`, `scripts/verify_browser.py` | Four counters with native record actions | Company metadata, quarantine counter, bounded OHLC and volume, preserved drill-downs |
| P02-AC-037–040 | `scripts/measure_odoo_p02.py`, `scripts/verify_odoo.ps1`, `scripts/verify_contention.py`, `tests/`, `docs/` | P01 verification inventory | Actual ORM workload, timed controls, expanded concurrency and refreshed audit evidence |

## 05 — Requirement traceability matrix

Original stable IDs are retained. Corrected descriptions distinguish prohibited functionality from delivered capabilities. Detailed P02 lines are tracked under new IDs, with their group-level statuses in section 13. [Standalone traceability](docs/REQUIREMENTS_TRACEABILITY.md)

| Requirement ID | Requirement | Status | Implementation | Test ID | Evidence | Remaining Work |
| --- | --- | --- | --- | --- | --- | --- |
| S01-001 | Principal Odoo 20 Community Architect | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-002 | Senior Python Software Engineer | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-003 | Quantitative Trading Researcher | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-004 | Financial Market Data Engineer | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-005 | Intraday Trading Strategy Researcher | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-006 | Statistical Modeling Specialist | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-007 | Machine Learning Engineer | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-008 | Portfolio Risk Management Specialist | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-009 | Angel One SmartAPI Integration Engineer | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-010 | PostgreSQL Performance Engineer | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-011 | Senior OWL JavaScript Developer | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-012 | Professional Financial Dashboard UX/UI Designer | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-013 | Cybersecurity Engineer | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-014 | Software Quality Assurance Engineer | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-015 | Automated Testing Engineer | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-016 | DevOps and Release Engineering Specialist | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-017 | Apply the documented research discipline, statistical methods, capital protection principles, and engineering practices associated with experienced professional traders and institutional quantitative research teams | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-018 | Do not claim to possess actual decades of trading experience, proprietary institutional strategies, or guaranteed profitable trading capabilities | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S01-019 | Do not merely provide architectural suggestions, sample code, pseudocode, or a development plan | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-001 | Product Name: Golok AI Trading Lab Pro | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-002 | Company: Golok Technology | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-003 | Technical Module Name: `golok_ai_trading_lab_pro` | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-004 | Platform: Odoo 20 Community Edition | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-005 | Backend: Python | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-006 | Database: PostgreSQL | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-007 | Frontend: Native Odoo OWL, JavaScript, XML, and SCSS | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-008 | Primary Market: Indian Equity Market | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-009 | Primary Exchange: NSE | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-010 | Secondary Exchange: BSE, subject to provider support | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-011 | Primary Broker Data Provider: Angel One SmartAPI | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-012 | Primary Trading Research Type: Intraday Equity Trading | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-013 | Secondary Research Types: Swing and Positional Trading | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-014 | Deployment: Localhost | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-015 | Timezone: Asia/Kolkata | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-016 | Currency: INR | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-017 | Hardware: CPU-only laptop | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-018 | Available RAM: 16 GB | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-019 | Dedicated GPU: Not available | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-020 | Paid AI APIs: Not available | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-021 | Local LLMs: Not required | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-022 | Target mandatory software subscription cost: Zero | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-023 | The product must operate without OpenAI API, Claude API, Gemini API, Ollama, DeepSeek, Qwen, or any other LLM dependency | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S02-024 | The word AI in the product name refers to computational intelligence, statistical research, adaptive strategy evaluation, and permitted lightweight machine learning | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S03-001 | Build a professional-grade quantitative stock market research and trading decision-support platform that identifies evidence-supported intraday trading opportunities | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S03-002 | The primary objective is not to generate the maximum number of tips | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S03-003 | Maximize sustainable risk-adjusted expected returns | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S03-004 | Identify statistically supported trading opportunities | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S03-005 | Minimize unnecessary and low-quality trades | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S03-006 | Protect trading capital | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S03-007 | Detect unfavorable market conditions | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S03-008 | Reject opportunities without sufficient evidence | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S03-009 | Account for actual trading costs | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S03-010 | Improve strategy evaluation through reproducible research | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S03-011 | Provide transparent trading recommendations | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S03-012 | Continuously measure actual strategy performance | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S03-013 | Never guarantee profits | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S03-014 | Never invent a profitability percentage, win rate, market price, financial result, or statistical confidence value | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S04-001 | The current product must be a research, recommendation, monitoring, backtesting, and paper trading platform | NOT_STARTED | — | — | — | Implement remaining research, paper and monitoring features, preserving the product boundary. |
| S04-002 | Retrieve authorized live market data | NOT_STARTED | — | — | — | Implement remaining research, paper and monitoring features, preserving the product boundary. |
| S04-003 | Retrieve historical market data | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | U01–U05, O03–O04 | `docs/evidence/tests/unit.log` | CSV workflow exists. Provider-backed history and independent source validation remain. |
| S04-004 | Research stocks | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | U01–U05, O03–O04 | `docs/evidence/tests/unit.log` | CSV workflow exists. Provider-backed history and independent source validation remain. |
| S04-005 | Generate trading recommendations | NOT_STARTED | — | — | — | Implement remaining research, paper and monitoring features, preserving the product boundary. |
| S04-006 | Suggest entry prices | NOT_STARTED | — | — | — | Implement remaining research, paper and monitoring features, preserving the product boundary. |
| S04-007 | Suggest stop-loss prices | NOT_STARTED | — | — | — | Implement remaining research, paper and monitoring features, preserving the product boundary. |
| S04-008 | Suggest target prices | NOT_STARTED | — | — | — | Implement remaining research, paper and monitoring features, preserving the product boundary. |
| S04-009 | Calculate suggested position sizes | NOT_STARTED | — | — | — | Implement remaining research, paper and monitoring features, preserving the product boundary. |
| S04-010 | Monitor active recommendations | NOT_STARTED | — | — | — | Implement remaining research, paper and monitoring features, preserving the product boundary. |
| S04-011 | Generate exit alerts | NOT_STARTED | — | — | — | Implement remaining research, paper and monitoring features, preserving the product boundary. |
| S04-012 | Simulate paper trades | NOT_STARTED | — | — | — | Implement remaining research, paper and monitoring features, preserving the product boundary. |
| S04-013 | Calculate hypothetical trading performance | NOT_STARTED | — | — | — | Implement remaining research, paper and monitoring features, preserving the product boundary. |
| S04-014 | Prohibited and absent — place real broker orders | CONSTRAINT_VERIFIED | `services/smartapi.py` | P02-SEC-01 | `docs/evidence/p02/unit/python.log` | Recheck when new paths are introduced. |
| S04-015 | Prohibited and absent — modify real broker orders | CONSTRAINT_VERIFIED | `services/smartapi.py` | P02-SEC-01 | `docs/evidence/p02/unit/python.log` | Recheck when new paths are introduced. |
| S04-016 | Prohibited and absent — cancel real broker orders | CONSTRAINT_VERIFIED | `services/smartapi.py` | P02-SEC-01 | `docs/evidence/p02/unit/python.log` | Recheck when new paths are introduced. |
| S04-017 | Prohibited and absent — automatically buy real shares | CONSTRAINT_VERIFIED | `services/smartapi.py` | P02-SEC-01 | `docs/evidence/p02/unit/python.log` | Recheck when new paths are introduced. |
| S04-018 | Prohibited and absent — automatically sell real shares | CONSTRAINT_VERIFIED | `services/smartapi.py` | P02-SEC-01 | `docs/evidence/p02/unit/python.log` | Recheck when new paths are introduced. |
| S04-019 | Prohibited and absent — transfer funds | CONSTRAINT_VERIFIED | `services/smartapi.py` | P02-SEC-01 | `docs/evidence/p02/unit/python.log` | Recheck when new paths are introduced. |
| S04-020 | Prohibited and absent — allocate real account capital automatically | CONSTRAINT_VERIFIED | `services/smartapi.py` | P02-SEC-01 | `docs/evidence/p02/unit/python.log` | Recheck when new paths are introduced. |
| S04-021 | Prohibited and absent — implement autonomous real-money trading | CONSTRAINT_VERIFIED | `services/smartapi.py` | P02-SEC-01 | `docs/evidence/p02/unit/python.log` | Recheck when new paths are introduced. |
| S04-022 | Hidden or dormant real-order execution is prohibited and absent | CONSTRAINT_VERIFIED | `services/smartapi.py` | P02-SEC-01 | `docs/evidence/p02/unit/python.log` | Recheck when new paths are introduced. |
| S05-001 | Inspect the existing repository | PARTIAL | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| S05-002 | Locate the actual Odoo installation | PARTIAL | See milestone report | — | Evidence and scope in report | Verify and document as subsequent slices land. |
| S05-003 | Identify Odoo version and edition | PARTIAL | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| S05-004 | Identify Python and PostgreSQL versions | PARTIAL | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| S05-005 | Inspect available hardware resources | PARTIAL | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| S05-006 | Detect operating system and CPU capabilities | PARTIAL | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| S05-007 | Inspect Git status | PARTIAL | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| S05-008 | Detect existing module files | PARTIAL | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| S05-009 | Preserve existing valid development | PARTIAL | See milestone report | — | Evidence and scope in report | Verify and document as subsequent slices land. |
| S05-010 | Identify installed dependencies | PARTIAL | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| S05-011 | Identify available testing infrastructure | PARTIAL | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| S05-012 | Verify access to official technical documentation | PARTIAL | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| S05-013 | `docs/MASTER_REQUIREMENTS.md` | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S05-014 | `docs/ARCHITECTURE.md` | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S05-015 | `docs/REQUIREMENTS_TRACEABILITY.md` | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S05-016 | `docs/DEVELOPMENT_PLAN.md` | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S05-017 | `docs/DECISION_LOG.md` | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S05-018 | `docs/RISK_REGISTER.md` | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S05-019 | Maintain these documents throughout development | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S05-020 | Implement in dependency order | PARTIAL | See milestone report | — | Evidence and scope in report | Verify and document as subsequent slices land. |
| S05-021 | Do not create a large collection of empty models, nonfunctional menus, placeholder methods, or unfinished features and claim completion | PARTIAL | See milestone report | — | Evidence and scope in report | Verify and document as subsequent slices land. |
| S05-022 | If the available execution context prevents completing the entire scope, prioritize the foundational and data-integrity components, document incomplete requirements precisely, and leave the project in a stable, testable state | PARTIAL | See milestone report | — | Evidence and scope in report | Verify and document as subsequent slices land. |
| S06-001 | Odoo business models | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-002 | Data provider adapters | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-003 | Instrument reference data | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-004 | Market data ingestion | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-005 | Historical data storage | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-006 | Data quality validation | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-007 | Feature engineering | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-008 | Quantitative research | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-009 | Strategy execution | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-010 | Statistical validation | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-011 | Signal generation | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-012 | Risk management | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-013 | Portfolio simulation | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-014 | Backtesting | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-015 | Paper trading | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-016 | Notifications | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-017 | Dashboard services | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-018 | Background research jobs | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-019 | Security | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-020 | Diagnostics | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-021 | Audit evidence | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-022 | Keep quantitative algorithms independently testable | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-023 | Avoid tightly coupling numerical calculations to the Odoo ORM | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-024 | Use versioned interfaces between the research engines and market data providers | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S06-025 | Do not use unsupported or obsolete APIs from earlier Odoo versions | NOT_STARTED | — | — | — | Implement the remaining architectural components behind versioned boundaries. |
| S07-001 | Optimize the entire application for a CPU-only machine with 16 GB RAM | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | U04, P01 | `docs/evidence/performance/services.csv` | Current paths are bounded and manual. Add bounded scheduling when implemented. |
| S07-002 | No LLM runtime | COMPLETE | `__manifest__.py`, `services/` | U01–U08 | `docs/evidence/tests/unit.log` | — |
| S07-003 | No GPU dependency | COMPLETE | `__manifest__.py`, `services/` | U01–U08 | `docs/evidence/tests/unit.log` | — |
| S07-004 | No mandatory cloud computing | COMPLETE | `__manifest__.py`, `services/` | U01–U08 | `docs/evidence/tests/unit.log` | — |
| S07-005 | No mandatory paid AI API | COMPLETE | `__manifest__.py`, `services/` | U01–U08 | `docs/evidence/tests/unit.log` | — |
| S07-006 | No mandatory external paid analytics service | NOT_STARTED | — | — | — | Measure and bound persistence, jobs, cache and system resources. |
| S07-007 | No unnecessary Redis, Kafka, Elasticsearch, or heavyweight distributed architecture | COMPLETE | `__manifest__.py`, `services/` | U01–U08 | `docs/evidence/tests/unit.log` | — |
| S07-008 | No unnecessary deep learning framework | COMPLETE | `__manifest__.py`, `services/` | U01–U08 | `docs/evidence/tests/unit.log` | — |
| S07-009 | No uncontrolled parallel execution | NOT_STARTED | — | — | — | Measure and bound persistence, jobs, cache and system resources. |
| S07-010 | No unbounded memory consumption | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | U04, P01 | `docs/evidence/performance/services.csv` | Current paths are bounded and manual. Add bounded scheduling when implemented. |
| S07-011 | NumPy | OPTIONAL | — | — | — | Technology option, excluded from functional coverage. |
| S07-012 | Pandas | OPTIONAL | — | — | — | Technology option, excluded from functional coverage. |
| S07-013 | SciPy | OPTIONAL | — | — | — | Technology option, excluded from functional coverage. |
| S07-014 | Scikit-learn | OPTIONAL | — | — | — | Technology option, excluded from functional coverage. |
| S07-015 | XGBoost with controlled CPU resources | OPTIONAL | — | — | — | Technology option, excluded from functional coverage. |
| S07-016 | Python standard library | OPTIONAL | — | — | — | Technology option, excluded from functional coverage. |
| S07-017 | PostgreSQL | OPTIONAL | — | — | — | Technology option, excluded from functional coverage. |
| S07-018 | Lightweight financial NLP dictionaries | OPTIONAL | — | — | — | Technology option, excluded from functional coverage. |
| S07-019 | Native Odoo scheduled actions | OPTIONAL | — | — | — | Technology option, excluded from functional coverage. |
| S07-020 | Bounded batch processing | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | U04, P01 | `docs/evidence/performance/services.csv` | Current paths are bounded and manual. Add bounded scheduling when implemented. |
| S07-021 | Configurable worker limits | NOT_STARTED | — | — | — | Measure and bound persistence, jobs, cache and system resources. |
| S07-022 | CPU thread limits | NOT_STARTED | — | — | — | Measure and bound persistence, jobs, cache and system resources. |
| S07-023 | Memory monitoring | NOT_STARTED | — | — | — | Measure and bound persistence, jobs, cache and system resources. |
| S07-024 | Configurable cache limits | NOT_STARTED | — | — | — | Measure and bound persistence, jobs, cache and system resources. |
| S07-025 | Incremental indicator calculations | NOT_STARTED | — | — | — | Measure and bound persistence, jobs, cache and system resources. |
| S07-026 | Efficient database indexes | NOT_STARTED | — | — | — | Measure and bound persistence, jobs, cache and system resources. |
| S07-027 | Bulk ingestion | NOT_STARTED | — | — | — | Measure and bound persistence, jobs, cache and system resources. |
| S07-028 | Historical data retention policies | NOT_STARTED | — | — | — | Measure and bound persistence, jobs, cache and system resources. |
| S07-029 | Graceful overload handling | NOT_STARTED | — | — | — | Measure and bound persistence, jobs, cache and system resources. |
| S07-030 | Background job recovery | NOT_STARTED | — | — | — | Measure and bound persistence, jobs, cache and system resources. |
| S07-031 | Persistent processing checkpoints | NOT_STARTED | — | — | — | Measure and bound persistence, jobs, cache and system resources. |
| S07-032 | Use performance measurements to establish realistic stock universe sizes and refresh intervals | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | U04, P01 | `docs/evidence/performance/services.csv` | Current paths are bounded and manual. Add bounded scheduling when implemented. |
| S07-033 | Do not claim that scanning 1,000 stocks at a particular frequency is supported until measured | NOT_STARTED | — | — | — | Measure and bound persistence, jobs, cache and system resources. |
| S08-001 | Use Angel One SmartAPI as the primary authorized market data provider | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-002 | https://smartapi.angelone.in/ | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-003 | https://smartapi.angelone.in/docs | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-004 | https://github.com/angel-one/smartapi-python | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-005 | Verify current documentation before implementation | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-006 | Verification date | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-007 | Supported authentication methods | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-008 | API pricing and access conditions | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-009 | Static IP requirements | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-010 | Data entitlement restrictions | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-011 | REST API rate limits | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-012 | WebSocket subscription limits | BLOCKED | — | B01 | See report §08 | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-013 | Historical data restrictions | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-014 | Session expiration behavior | BLOCKED | — | B01 | See report §08 | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-015 | Supported exchanges and instrument types | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-016 | Secure credential configuration | BLOCKED | — | B01 | See report §08 | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-017 | Session authentication | BLOCKED | — | B01 | See report §08 | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-018 | Session renewal or controlled reauthentication | BLOCKED | — | B01 | See report §08 | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-019 | Instrument master synchronization | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-020 | Instrument token mapping | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-021 | Historical candle retrieval | BLOCKED | — | B01 | See report §08 | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-022 | Live quote retrieval | BLOCKED | — | B01 | See report §08 | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-023 | WebSocket market data ingestion | BLOCKED | — | B01 | See report §08 | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-024 | Heartbeat monitoring | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-025 | Reconnection management | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-026 | Subscription management | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-027 | Exponential backoff | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-028 | Provider health monitoring | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-029 | Rate-limit-aware request scheduling | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-030 | Error classification | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-031 | Connectivity diagnostics | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-032 | Do not bypass broker restrictions, authentication requirements, static IP requirements, or subscription conditions | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-033 | Do not expose secrets in frontend assets, screenshots, source control, logs, exception messages, or reports | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-034 | Use environment-based secrets or an appropriately protected local secret store | NOT_STARTED | — | — | — | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-035 | The application must install and operate in simulation mode without real broker credentials | BLOCKED | — | B01 | See report §08 | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S08-036 | If credentials are unavailable, mark real integration testing as BLOCKED. Mock or fixture testing must not be represented as successful live API verification | BLOCKED | — | B01 | See report §08 | Verify official limits and account entitlement. Implement and test the read-only adapter. |
| S09-001 | Duplicate candles | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03–O04, O08 | `docs/evidence/installation/{fresh,upgrade}.log`, `docs/evidence/security/contention.log` | — |
| S09-002 | Missing candles | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | U01–U05, O03–O04 | `docs/evidence/tests/unit.log` | CSV workflow exists. Provider-backed history and independent source validation remain. |
| S09-003 | Invalid prices | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| S09-004 | Negative or invalid volume | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| S09-005 | Invalid OHLC relationships | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| S09-006 | Out-of-order ticks | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-007 | Incorrect instrument mappings | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-008 | Incorrect timestamps | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| S09-009 | Future-dated observations | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| S09-010 | Stale market data | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-011 | Incomplete candles | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-012 | Missing trading sessions | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-013 | Provider disconnects | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-014 | Corporate actions | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-015 | Stock splits | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-016 | Bonus issues | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-017 | Delisted and suspended instruments | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-018 | Exchange calendar differences | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-019 | Trading holidays | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-020 | Special trading sessions | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-021 | Data source | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| S09-022 | Exchange | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| S09-023 | Instrument identifier | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| S09-024 | Market timestamp | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| S09-025 | Ingestion timestamp | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| S09-026 | Data interval | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| S09-027 | Quality status | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| S09-028 | Data freshness | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-029 | Processing version | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| S09-030 | Distinguish real, delayed, historical, imported, and synthetic fixture data | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-031 | Do not silently substitute delayed data for real-time data | NOT_STARTED | — | — | — | Add calendar, reference data, corporate actions, data freshness and provider fault handling. |
| S09-032 | Implement idempotent ingestion and prevent duplicate records using database-backed constraints | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03–O04, O08 | `docs/evidence/installation/{fresh,upgrade}.log`, `docs/evidence/security/contention.log` | — |
| S09-033 | Provide controlled historical import support using legally authorized datasets | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| S10-001 | Create a standardized interface for the following 25 research capabilities | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-01 | Technical Analysis | PARTIAL | `services/research.py`, `models/lab.py` | U06–U08, O05–O06 | `docs/evidence/tests/unit.log` | Three descriptive findings exist. Complete the remaining indicator set, evidence contract and engine methods. |
| RE-02 | Fundamental Analysis | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-03 | Price Action Analysis | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-04 | Candlestick Pattern Analysis | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-05 | Volume Intelligence | PARTIAL | `services/research.py`, `models/lab.py` | U06–U08, O05–O06 | `docs/evidence/tests/unit.log` | Three descriptive findings exist. Complete the remaining indicator set, evidence contract and engine methods. |
| RE-06 | Support and Resistance | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-07 | Breakout Detection | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-08 | False Breakout Detection | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-09 | Market Trend Analysis | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-10 | Sector Performance and Rotation | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-11 | Benchmark Index Analysis | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-12 | Global Market Context | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-13 | Financial News and Event Analysis | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-14 | Institutional Activity Proxies | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-15 | Historical Pattern Analysis | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-16 | Statistical Probability Estimation | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-17 | Liquidity Analysis | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-18 | Volatility Analysis | PARTIAL | `services/research.py`, `models/lab.py` | U06–U08, O05–O06 | `docs/evidence/tests/unit.log` | Three descriptive findings exist. Complete the remaining indicator set, evidence contract and engine methods. |
| RE-19 | Momentum Analysis | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-20 | Abnormal Market Activity Detection | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-21 | Entry Optimization | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-22 | Stop-Loss Optimization | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-23 | Profit Target Optimization | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-24 | Historical Strategy Performance | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| RE-25 | Net Expected Profit and Risk Validation | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-002 | Engine identifier | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-003 | Engine version | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-004 | Instrument | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-005 | Research timestamp | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-006 | Required input data | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-007 | Input data freshness | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-008 | Observed findings | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-009 | Supporting evidence | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-010 | Contradictory evidence | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-011 | Applicable strategy | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-012 | Research score, if applicable | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-013 | Known limitations | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-014 | Missing data | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-015 | Quality warnings | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-016 | Execution duration | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-017 | Result status | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-018 | COMPLETED | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-019 | NOT_APPLICABLE | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-020 | INSUFFICIENT_DATA | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-021 | STALE_DATA | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-022 | ERROR | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-023 | Do not assign positive default scores when data is missing | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-024 | Do not pretend to know institutional order flow when only indirect proxies are available | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-025 | Do not claim market manipulation has been established solely from abnormal price or volume behavior | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S10-026 | Do not force every research capability to influence every intraday signal. Apply relevant engines according to strategy type and data availability | NOT_STARTED | — | — | — | Complete the engine contract and independently verify relevant engines. |
| S11-001 | Implement mathematically correct, independently tested indicators | PARTIAL | `services/research.py`, `models/lab.py` | U06–U08, O05–O06 | `docs/evidence/tests/unit.log` | Three descriptive findings exist. Complete the remaining indicator set, evidence contract and engine methods. |
| S11-002 | SMA | PARTIAL | `services/research.py`, `models/lab.py` | U06–U08, O05–O06 | `docs/evidence/tests/unit.log` | Three descriptive findings exist. Complete the remaining indicator set, evidence contract and engine methods. |
| S11-003 | EMA | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-004 | RSI | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-005 | MACD | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-006 | ATR | PARTIAL | `services/research.py`, `models/lab.py` | U06–U08, O05–O06 | `docs/evidence/tests/unit.log` | Three descriptive findings exist. Complete the remaining indicator set, evidence contract and engine methods. |
| S11-007 | VWAP | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-008 | ADX | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-009 | Bollinger Bands | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-010 | Stochastic Oscillator | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-011 | Relative Volume | PARTIAL | `services/research.py`, `models/lab.py` | U06–U08, O05–O06 | `docs/evidence/tests/unit.log` | Three descriptive findings exist. Complete the remaining indicator set, evidence contract and engine methods. |
| S11-012 | Rate of Change | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-013 | On-Balance Volume | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-014 | Historical Volatility | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-015 | Rolling Highs and Lows | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-016 | Opening Range | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-017 | Relative Strength | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-018 | Price Gaps | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-019 | Volume Spikes | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-020 | Trend Slopes | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-021 | 1 minute | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-022 | 3 minutes | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-023 | 5 minutes | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-024 | 15 minutes | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-025 | 30 minutes | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-026 | 1 hour | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-027 | Daily | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-028 | Respect provider availability and data granularity | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-029 | Never generate misleading values from insufficient historical observations | NOT_STARTED | — | — | — | Implement and test remaining indicators and time/session behavior. |
| S11-030 | Prevent look-ahead bias in every indicator and feature calculation | PARTIAL | `services/research.py`, `models/lab.py` | U07, O05 | `docs/evidence/tests/unit.log` | Close-time cutoff proven by snapshot assertion if ORM passes. Point-in-time vendor availability, survivorship and future execution tests remain. |
| S12-001 | Implement a versioned and extensible strategy framework | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-01 | Opening Range Breakout | PARTIAL | `services/backtest.py` | P02-BT-01 | `docs/evidence/p02/backtesting/synthetic.json` | Synthetic only. No financial validation. |
| ST-02 | VWAP Pullback | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-03 | VWAP Reclaim | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-04 | Trend Following | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-05 | Momentum Continuation | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-06 | Volume Confirmed Breakout | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-07 | Support and Resistance Breakout | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-08 | Mean Reversion | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-09 | Gap Continuation | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-10 | Gap Reversal | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-11 | Multi-Timeframe Trend Confirmation | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-12 | Relative Strength Momentum | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-13 | Sector Rotation | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-14 | Volatility Compression Breakout | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-15 | Trend Pullback | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-16 | False Breakout Reversal | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-17 | Statistical Reversion | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-18 | ATR-Based Channel Breakout | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-19 | Momentum Exhaustion | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| ST-20 | Market Regime Adaptive Strategy | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S12-002 | Applicable market conditions | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S12-003 | Required data | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S12-004 | Entry conditions | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S12-005 | Exit conditions | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S12-006 | Stop-loss methodology | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S12-007 | Target methodology | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S12-008 | Invalidation conditions | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S12-009 | Position sizing constraints | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S12-010 | Applicable timeframes | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S12-011 | Supported instruments | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S12-012 | Trading costs | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S12-013 | Historical validation requirements | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S12-014 | Strategy version | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S12-015 | Never enable a strategy merely because its implementation exists | NOT_STARTED | — | — | — | Implement and independently validate a versioned research-only candidate. |
| S13-001 | Bullish trends | NOT_STARTED | — | — | — | Implement and verify regime classification on real datasets. |
| S13-002 | Bearish trends | NOT_STARTED | — | — | — | Implement and verify regime classification on real datasets. |
| S13-003 | Sideways markets | NOT_STARTED | — | — | — | Implement and verify regime classification on real datasets. |
| S13-004 | High-volatility markets | NOT_STARTED | — | — | — | Implement and verify regime classification on real datasets. |
| S13-005 | Low-volatility markets | NOT_STARTED | — | — | — | Implement and verify regime classification on real datasets. |
| S13-006 | Strong momentum conditions | NOT_STARTED | — | — | — | Implement and verify regime classification on real datasets. |
| S13-007 | Weak momentum conditions | NOT_STARTED | — | — | — | Implement and verify regime classification on real datasets. |
| S13-008 | Market stress | NOT_STARTED | — | — | — | Implement and verify regime classification on real datasets. |
| S13-009 | Abnormal market conditions | NOT_STARTED | — | — | — | Implement and verify regime classification on real datasets. |
| S13-010 | Insufficient evidence | NOT_STARTED | — | — | — | Implement and verify regime classification on real datasets. |
| S13-011 | Use observable market data and transparent quantitative methods | NOT_STARTED | — | — | — | Implement and verify regime classification on real datasets. |
| S13-012 | Avoid forcing trend-following strategies into unsuitable range-bound conditions | NOT_STARTED | — | — | — | Implement and verify regime classification on real datasets. |
| S13-013 | Avoid treating a regime classification as a guaranteed future market direction | NOT_STARTED | — | — | — | Implement and verify regime classification on real datasets. |
| S13-014 | Implement a configurable market-wide NO TRADE decision when market quality deteriorates | NOT_STARTED | — | — | — | Implement and verify regime classification on real datasets. |
| S14-001 | Gathering applicable research results | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-002 | Validating data availability | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-003 | Checking strategy eligibility | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-004 | Checking strategy historical performance | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-005 | Evaluating liquidity | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-006 | Evaluating volatility | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-007 | Evaluating market regime | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-008 | Detecting contradictory evidence | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-009 | Calculating expected net profitability | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-010 | Evaluating estimated downside | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-011 | Checking entry quality | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-012 | Validating stop loss | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-013 | Validating target feasibility | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-014 | Checking risk-to-reward | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-015 | Checking recommendation freshness | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-016 | Applying hard rejection rules | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-017 | Ranking eligible candidates | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-018 | Generating explainable decisions | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-019 | BUY | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-020 | SELL / SHORT OPPORTUNITY | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-021 | WATCH | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-022 | WAIT FOR ENTRY | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-023 | HOLD EXISTING POSITION | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-024 | EXIT | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-025 | NO TRADE | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-026 | INVALIDATED | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-027 | EXPIRED | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-028 | Do not treat correlated technical indicators as independent confirmation | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-029 | Do not require arbitrary unanimous agreement across unrelated research engines | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S14-030 | Do not use arbitrary weighted scores as proof of probability | NOT_STARTED | — | — | — | Implement strategy, data and risk eligibility before actionable recommendation states. |
| S15-001 | Implement a transparent, configurable scoring framework | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-002 | A+: 95–100 | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-003 | A: 90–94 | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-004 | B: 85–89 | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-005 | Watchlist: 80–84 | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-006 | Rejected: Below 80 | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-007 | Configurable weighting | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-008 | Strategy-specific scoring | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-009 | Missing-data handling | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-010 | Negative evidence penalties | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-011 | Score decomposition | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-012 | Versioned score configuration | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-013 | Historical score-performance analysis | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-014 | Calibration analysis | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-015 | Threshold sensitivity analysis | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-016 | Research quality score | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-017 | Expert-system agreement | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-018 | Historical observed win rate | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-019 | Calibrated estimated probability | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-020 | Expected return | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-021 | Statistical uncertainty | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S15-022 | Never display a score of 95/100 as a 95% chance of profit | NOT_STARTED | — | — | — | Implement explainable scoring and test calibration after historical and holdout datasets exist. |
| S16-001 | The objective is positive, sustainable net trading expectancy, not maximum historical win rate | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-002 | Gross return | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-003 | Net return | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-004 | Average winning trade | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-005 | Average losing trade | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-006 | Win rate | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-007 | Loss rate | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-008 | Expected value per trade | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-009 | Profit factor | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-010 | Maximum drawdown | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-011 | Risk-to-reward ratio | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-012 | Sharpe ratio where statistically meaningful | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-013 | Sortino ratio where statistically meaningful | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-014 | Downside risk | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-015 | Turnover | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-016 | Consecutive losses | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-017 | Maximum adverse excursion | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-018 | Maximum favorable excursion | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-019 | Sample size | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-020 | Confidence intervals | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-021 | Performance stability across market regimes | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-022 | Extend this methodology appropriately for neutral outcomes and variable exits | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-023 | Avoid double-counting transaction costs | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-024 | When sample sizes are insufficient, return insufficient evidence instead of fabricated confidence | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-025 | Implement conservative uncertainty handling | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S16-026 | Reject strategies with weak out-of-sample evidence, unacceptable drawdowns, excessive sensitivity, or negative expected net returns | NOT_STARTED | — | — | — | Implement metrics and uncertainty handling on verified experiment results. |
| S17-001 | Build a configurable Indian equity trading cost model | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-002 | Brokerage | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-003 | Securities Transaction Tax | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-004 | Exchange transaction charges | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-005 | SEBI charges | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-006 | GST | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-007 | Stamp duty | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-008 | Bid-ask spread | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-009 | Slippage | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-010 | Other applicable verified costs | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-011 | Effective date | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-012 | Instrument type | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-013 | Transaction side | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-014 | Source | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-015 | Verification status | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-016 | Do not hardcode unverified current statutory charges | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-017 | If actual cost settings have not been verified, clearly label the output as an estimate | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S17-018 | Do not calculate misleading net profit by ignoring material execution costs | NOT_STARTED | — | — | — | Collect verified tariff inputs and build an effective-dated cost engine. |
| S18-001 | Implement independently enforceable risk rules | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-002 | Maximum planned risk per trade: 0.5% of configured capital | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-003 | Maximum planned daily loss threshold: 1% | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-004 | Maximum daily paper-trade entries: 3 | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-005 | Consecutive loss pause threshold: 2 | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-006 | Minimum planned risk-to-reward: 1:2 | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-007 | Preferred candidate risk-to-reward: 1:3 | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-008 | Leverage: Disabled | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-009 | Averaging losing positions: Disabled | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-010 | Martingale strategies: Prohibited | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-011 | Unlimited position sizing: Prohibited | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-012 | Overnight intraday positions: Prohibited in simulation policy | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-013 | Risk-based position sizing | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-014 | Capital-based position limits | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-015 | Liquidity constraints | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-016 | Stop-loss distance validation | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-017 | Tick-size validation | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-018 | Volatility-based risk adjustment | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-019 | Portfolio exposure tracking | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-020 | Correlation risk | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-021 | Sector concentration limits | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-022 | Market-wide risk filters | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-023 | Daily loss monitoring | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-024 | Consecutive loss detection | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-025 | Strategy suspension | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-026 | Research suspension | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-027 | Paper trading kill switch | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-028 | Use explicit reference capital for suggested position sizing | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S18-029 | Account for estimated fees and adverse execution where appropriate | NOT_STARTED | — | — | — | Implement independent capital vetoes and risk sizing on cost-aware paper data. |
| S19-001 | Build a reproducible, event-aware backtesting framework | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-002 | Chronological data processing | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-003 | No future data leakage | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-004 | No look-ahead bias | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-005 | Survivorship bias controls | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-006 | Corporate action handling | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-007 | Realistic entry timing | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-008 | Realistic exit timing | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-009 | Bid-ask spread modeling | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-010 | Transaction cost modeling | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-011 | Slippage modeling | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-012 | Liquidity constraints | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-013 | Stop-loss execution assumptions | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-014 | Market session boundaries | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-015 | Trading holiday handling | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-016 | Partial fill modeling where supported | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-017 | Reproducible strategy parameters | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-018 | Do not assume entry at a candle price that was unavailable when the decision was made | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-019 | If both target and stop loss are crossed inside the same candle and execution order cannot be determined, apply a documented conservative ambiguity policy or use finer-grained data | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-020 | Do not automatically assume the profitable outcome | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-021 | In-sample training | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-022 | Out-of-sample evaluation | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-023 | Walk-forward testing | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-024 | Time-series cross-validation | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-025 | Parameter sensitivity analysis | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-026 | Stress testing | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-027 | Monte Carlo or appropriate block-bootstrap analysis | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-028 | Benchmark comparison | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-029 | Reproducible experiment identifiers | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-030 | Do not optimize strategy parameters against the final holdout dataset | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S19-031 | Do not report simulated returns as actual realized returns | NOT_STARTED | — | — | — | Implement chronological backtesting with calendar, cost, execution and holdout tests. |
| S20-001 | Logistic regression | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-002 | Random forest with controlled depth | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-003 | Gradient boosting | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-004 | CPU-optimized XGBoost | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-005 | Lightweight regime classification | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-006 | Statistical probability calibration | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-007 | Time-aware train/test separation | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-008 | Feature versioning | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-009 | Model versioning | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-010 | Reproducible random seeds | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-011 | Training data provenance | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-012 | Leakage detection | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-013 | Class imbalance analysis | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-014 | Probability calibration | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-015 | Model drift monitoring | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-016 | Model performance tracking | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-017 | Safe model rollback | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-018 | Avoid uncontrolled hyperparameter search | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-019 | Reject complex models that fail to demonstrate meaningful improvement | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S20-020 | Never automatically promote an experimental model into actionable signal generation | NOT_STARTED | — | — | — | Evaluate the need for ML against transparent baselines after data and strategies are validated. |
| S21-001 | Create a realistic paper trading environment | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-002 | Virtual trading accounts | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-003 | Opening balance | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-004 | Available virtual cash | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-005 | Reserved cash | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-006 | Simulated orders | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-007 | Simulated executions | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-008 | Open positions | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-009 | Closed positions | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-010 | Simulated stop-loss exits | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-011 | Simulated profit targets | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-012 | Partial profit booking | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-013 | Trailing stop logic | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-014 | Intraday square-off | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-015 | Realistic transaction costs | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-016 | Daily realized P&L | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-017 | Unrealized P&L | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-018 | Net virtual equity | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-019 | Drawdown tracking | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-020 | Trading journal | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-021 | All balances and transactions must be explicitly identified as virtual | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-022 | Use consistent, auditable accounting rules for virtual cash and positions | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-023 | Prevent duplicate executions | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-024 | Ensure atomic state transitions | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S21-025 | Never connect paper-trading execution to real broker order APIs | NOT_STARTED | — | — | — | Build an atomic virtual ledger, fill policy and restart recovery. |
| S22-001 | Unique Signal ID | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-002 | Instrument name and symbol | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-003 | Exchange | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-004 | Strategy name and version | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-005 | Trading type | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-006 | BUY or permitted SELL direction | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-007 | Generation time in IST | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-008 | Validity expiry | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-009 | Latest verified price | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-010 | Price observation timestamp | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-011 | Entry range | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-012 | Stop-loss price | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-013 | Target 1 | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-014 | Target 2, if justified | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-015 | Target 3, if justified | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-016 | Suggested quantity | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-017 | Required capital | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-018 | Estimated gross profit | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-019 | Estimated net profit | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-020 | Estimated planned loss | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-021 | Trading cost assumptions | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-022 | Planned risk-to-reward | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-023 | Research quality score | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-024 | Supporting evidence | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-025 | Contradictory evidence | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-026 | Historical performance reference | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-027 | Sample size | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-028 | Relevant market conditions | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-029 | Risk warnings | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-030 | Data quality status | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-031 | Signal invalidation conditions | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-032 | Do not invent multiple targets solely to populate the UI | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-033 | Do not generate a precise estimated win probability without sufficient statistical calibration | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-034 | Provide an explanation of why the trade qualifies | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S22-035 | Provide an explanation of why rejected candidates failed | NOT_STARTED | — | — | — | Implement actionable data and explainability fields before enabling recommendations. |
| S23-001 | Entry zone reached | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-002 | Entry no longer valid | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-003 | Excessive price movement | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-004 | Target reached | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-005 | Stop-loss threshold reached | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-006 | Trailing stop update | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-007 | Market reversal | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-008 | Liquidity deterioration | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-009 | Market data disconnect | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-010 | Signal expiry | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-011 | Intraday session closing | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-012 | Strategy invalidation | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-013 | New qualified opportunity | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-014 | Wait for entry | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-015 | Entry opportunity available | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-016 | Target observation | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-017 | Stop-loss warning | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-018 | Exit suggestion | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-019 | Recommendation invalidated | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-020 | Emergency market warning | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-021 | NO TRADE condition | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-022 | Support optional manual recording of actual user trades, clearly separated from paper-trade records | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S23-023 | Do not expose real-order execution functionality | NOT_STARTED | — | — | — | Add observation and expiry events after the signal and live data foundations. |
| S24-001 | Build an elegant, professional financial trading research interface under the Golok Technology brand | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-002 | The dashboard must be functional and backed by verified database records | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-003 | Do not build a static HTML mockup and claim that the dashboard is completed | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-004 | Use native Odoo 20 Community-compatible OWL components | PARTIAL | `static/src/`, `views/lab.xml`, `models/lab.py` | UI-01–UI-04 | `docs/evidence/browser/edge.log` | Historical overview and native lists exist. Dashboards A–I remain incomplete. |
| S24-005 | Excellent information hierarchy | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-006 | Professional typography | PARTIAL | `static/src/`, `views/lab.xml`, `models/lab.py` | UI-01–UI-04 | `docs/evidence/browser/edge.log` | Historical overview and native lists exist. Dashboards A–I remain incomplete. |
| S24-007 | Consistent spacing | PARTIAL | `static/src/`, `views/lab.xml`, `models/lab.py` | UI-01–UI-04 | `docs/evidence/browser/edge.log` | Historical overview and native lists exist. Dashboards A–I remain incomplete. |
| S24-008 | Clean financial charts | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-009 | Meaningful status colors | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-010 | Responsive layout | PARTIAL | `static/src/`, `views/lab.xml`, `models/lab.py` | UI-01–UI-04 | `docs/evidence/browser/edge.log` | Historical overview and native lists exist. Dashboards A–I remain incomplete. |
| S24-011 | Light and dark theme compatibility where supported | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-012 | Accessible controls | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-013 | Loading states | PARTIAL | `static/src/`, `views/lab.xml`, `models/lab.py` | UI-01–UI-04 | `docs/evidence/browser/edge.log` | Historical overview and native lists exist. Dashboards A–I remain incomplete. |
| S24-014 | Empty states | PARTIAL | `static/src/`, `views/lab.xml`, `models/lab.py` | UI-01–UI-04 | `docs/evidence/browser/edge.log` | Historical overview and native lists exist. Dashboards A–I remain incomplete. |
| S24-015 | Error states | PARTIAL | `static/src/`, `views/lab.xml`, `models/lab.py` | UI-01–UI-04 | `docs/evidence/browser/edge.log` | Historical overview and native lists exist. Dashboards A–I remain incomplete. |
| S24-016 | Stale-data warnings | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-017 | Clear timestamps | PARTIAL | `static/src/`, `views/lab.xml`, `models/lab.py` | UI-01–UI-04 | `docs/evidence/browser/edge.log` | Historical overview and native lists exist. Dashboards A–I remain incomplete. |
| S24-018 | Smooth, bounded refresh behavior | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-019 | Avoid unnecessary animation, oversized graphics, heavy frontend frameworks, and unnecessary CDN dependencies | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-020 | Nifty 50 | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-021 | Bank Nifty | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-022 | Other available authorized benchmark indices | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-023 | Market status | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-024 | Market breadth | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-025 | Advancing and declining instruments | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-026 | Market regime | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-027 | Volatility status | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-028 | Sector performance | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-029 | Market data freshness | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-030 | Total eligible instruments | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-031 | Instruments scanned | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-032 | Instruments awaiting research | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-033 | Instruments rejected | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-034 | Qualified candidates | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-035 | Active strategies | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-036 | Research execution status | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-037 | Data quality failures | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-038 | Research duration | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-039 | Include filterable, sortable instrument tables | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-040 | Ranked trading opportunities | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-041 | Signal direction | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-042 | Research score | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-043 | Entry range | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-044 | Stop loss | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-045 | Profit targets | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-046 | Estimated net return | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-047 | Planned risk | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-048 | Risk-to-reward | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-049 | Validity | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-050 | Research evidence | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-051 | Candlestick chart | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-052 | Volume chart | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-053 | Relevant technical indicator overlays | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-054 | Support and resistance levels | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-055 | Strategy analysis | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-056 | Entry and exit levels | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-057 | Multi-timeframe research | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-058 | Applicable research engine results | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-059 | Positive and negative evidence | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-060 | Data quality status | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-061 | Use efficiently aggregated and bounded chart data | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-062 | Initial virtual capital | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-063 | Available virtual capital | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-064 | Current equity | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-065 | Open virtual positions | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-066 | Closed virtual positions | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-067 | Realized virtual P&L | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-068 | Unrealized virtual P&L | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-069 | Net virtual return | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-070 | Equity curve | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-071 | Drawdown curve | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-072 | Daily performance | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-073 | Trading journal | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-074 | Strategy performance ranking | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-075 | Historical win rates | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-076 | Net expectancy | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-077 | Sample sizes | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-078 | Maximum drawdowns | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-079 | Profit factor | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-080 | Market regime performance | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-081 | Out-of-sample results | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-082 | Validation status | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-083 | Active and suspended strategies | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-084 | Configured risk limits | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-085 | Current paper portfolio exposure | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-086 | Daily loss threshold | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-087 | Consecutive losses | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-088 | Sector concentration | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-089 | Risk rejection reasons | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-090 | Market-wide warnings | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-091 | Paper trading suspension state | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-092 | Angel One connectivity | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-093 | Market data provider status | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-094 | Session status | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-095 | WebSocket status | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-096 | Last successful data update | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-097 | Data lag | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-098 | Background job queue | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-099 | CPU utilization | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-100 | Memory utilization | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-101 | Storage usage | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-102 | Research errors | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-103 | Last completed research cycle | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-104 | Market summary | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-105 | Qualified opportunities | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-106 | Rejected opportunities | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-107 | Rejection reasons | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-108 | Most relevant research findings | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-109 | Paper trading performance | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-110 | Strategy warnings | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-111 | Data limitations | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-112 | Market risk conditions | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S24-113 | All KPI values must have documented and testable calculation definitions | PARTIAL | `static/src/`, `views/lab.xml`, `models/lab.py` | UI-01–UI-04 | `docs/evidence/browser/edge.log` | Historical overview and native lists exist. Dashboards A–I remain incomplete. |
| S24-114 | Every drill-down must apply correct access controls and filters | PARTIAL | `static/src/`, `views/lab.xml`, `models/lab.py` | UI-01–UI-04 | `docs/evidence/browser/edge.log` | Historical overview and native lists exist. Dashboards A–I remain incomplete. |
| S24-115 | Never show fake live prices or fictional performance as genuine | NOT_STARTED | — | — | — | Add remaining native OWL views and verify KPI definitions, charts and access. |
| S25-001 | Implement timezone-aware research scheduling | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-002 | Pre-market research | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-003 | Market opening analysis | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-004 | Intraday research cycles | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-005 | Signal monitoring | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-006 | Market closing research | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-007 | Daily paper trading reports | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-008 | Historical data synchronization | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-009 | Data quality maintenance | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-010 | Strategy performance review | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-011 | Use verified exchange trading sessions | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-012 | Respect weekends, holidays, and special sessions | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-013 | Persistent job status | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-014 | Job locking | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-015 | Retry policies | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-016 | Duplicate-job protection | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-017 | Timeout handling | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-018 | Failure recovery | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-019 | Scheduler monitoring | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-020 | Missed-job handling | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-021 | Prevent overlapping research jobs from corrupting data or exhausting CPU resources | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S25-022 | Do not assume localhost jobs run when the laptop is powered off or asleep | NOT_STARTED | — | — | — | Build exchange-aware scheduled jobs, locking, monitoring and recovery. |
| S26-001 | Record original recommendations | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S26-002 | Preserve the original research inputs | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S26-003 | Preserve original strategy and configuration versions | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S26-004 | Record subsequent observable outcomes | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S26-005 | Evaluate successful and unsuccessful recommendations | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S26-006 | Analyze performance by market regime | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S26-007 | Analyze score quality | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S26-008 | Identify statistically meaningful improvements | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S26-009 | Create experimental strategy versions | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S26-010 | Validate experimental versions independently | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S26-011 | Compare against the existing baseline | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S26-012 | Require explicit approval before promotion | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S26-013 | Never rewrite historical recommendations to make performance appear better | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S26-014 | Never silently change the original entry, stop loss, or target after observing the outcome | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S26-015 | Record amendments as new auditable events | NOT_STARTED | — | — | — | Preserve prospective outcomes and test promotion governance. |
| S27-001 | Trading Research Viewer | PARTIAL | `security/ir.access.csv`, `models/lab.py` | O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Add regression checks for future features and independent API calls. |
| S27-002 | Trading Research Analyst | PARTIAL | `security/ir.access.csv`, `models/lab.py` | O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Add regression checks for future features and independent API calls. |
| S27-003 | Trading Risk Manager | PARTIAL | `security/ir.access.csv`, `models/lab.py` | O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Add regression checks for future features and independent API calls. |
| S27-004 | Trading System Administrator | PARTIAL | `security/ir.access.csv`, `models/lab.py` | O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Add regression checks for future features and independent API calls. |
| S27-005 | Model access controls | COMPLETE | `security/ir.access.csv`, `models/lab.py` | O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Add regression checks for future features and independent API calls. |
| S27-006 | Record rules | COMPLETE | `security/ir.access.csv`, `models/lab.py` | O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Add regression checks for future features and independent API calls. |
| S27-007 | Company isolation | COMPLETE | `security/ir.access.csv`, `models/lab.py` | O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Add regression checks for future features and independent API calls. |
| S27-008 | Server-side authorization | COMPLETE | `security/ir.access.csv`, `models/lab.py` | O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Add regression checks for future features and independent API calls. |
| S27-009 | Protected configuration | NOT_STARTED | — | — | — | Extend current access controls with operational audit and independent concurrency tests. |
| S27-010 | Secret redaction | NOT_STARTED | — | — | — | Extend current access controls with operational audit and independent concurrency tests. |
| S27-011 | Input validation | NOT_STARTED | — | — | — | Extend current access controls with operational audit and independent concurrency tests. |
| S27-012 | Safe SQL usage | NOT_STARTED | — | — | — | Extend current access controls with operational audit and independent concurrency tests. |
| S27-013 | Secure controller routes | NOT_STARTED | — | — | — | Extend current access controls with operational audit and independent concurrency tests. |
| S27-014 | Audit logging | NOT_STARTED | — | — | — | Extend current access controls with operational audit and independent concurrency tests. |
| S27-015 | Sensitive field restrictions | NOT_STARTED | — | — | — | Extend current access controls with operational audit and independent concurrency tests. |
| S27-016 | Do not rely solely on frontend visibility for security | NOT_STARTED | — | — | — | Extend current access controls with operational audit and independent concurrency tests. |
| S27-017 | Avoid unsafe unrestricted `sudo()` usage | NOT_STARTED | — | — | — | Extend current access controls with operational audit and independent concurrency tests. |
| S27-018 | Do not expose broker tokens to ordinary users | NOT_STARTED | — | — | — | Extend current access controls with operational audit and independent concurrency tests. |
| S27-019 | Use database constraints where required | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03–O04, O08 | `docs/evidence/installation/{fresh,upgrade}.log`, `docs/evidence/security/contention.log` | — |
| S27-020 | Protect against duplicate ingestion, duplicate research runs, duplicate signals, and duplicate simulated executions | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03–O04, O08 | `docs/evidence/installation/{fresh,upgrade}.log`, `docs/evidence/security/contention.log` | — |
| S27-021 | Do not mutate real Odoo accounting records or real broker funds | NOT_STARTED | — | — | — | Extend current access controls with operational audit and independent concurrency tests. |
| INV-01 | No real broker order execution | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-02 | No mandatory paid AI dependency | COMPLETE | `__manifest__.py`, `services/` | U01–U08 | `docs/evidence/tests/unit.log` | — |
| INV-03 | No GPU dependency | COMPLETE | `__manifest__.py`, `services/` | U01–U08 | `docs/evidence/tests/unit.log` | — |
| INV-04 | No fabricated live market data | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-05 | No actionable signal from stale required data | GUARD_ONLY | `services/research.py`, `models/lab.py` | O05–O06 | `docs/evidence/installation/{fresh,upgrade}.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-06 | No look-ahead bias | PARTIAL | `services/research.py`, `models/lab.py` | U07, O05 | `docs/evidence/tests/unit.log` | Close-time cutoff proven by snapshot assertion if ORM passes. Point-in-time vendor availability, survivorship and future execution tests remain. |
| INV-07 | No future information in historical decisions | PARTIAL | `services/research.py`, `models/lab.py` | U07, O05 | `docs/evidence/tests/unit.log` | Close-time cutoff proven by snapshot assertion if ORM passes. Point-in-time vendor availability, survivorship and future execution tests remain. |
| INV-08 | No duplicate market data records | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03–O04, O08 | `docs/evidence/installation/{fresh,upgrade}.log`, `docs/evidence/security/contention.log` | — |
| INV-09 | No duplicate paper-trade execution | NOT_STARTED | — | — | — | Required when virtual execution, costs and sizing are implemented. |
| INV-10 | No misleading profit guarantees | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-11 | No uncalibrated score represented as probability | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-12 | No unauthorized broker credential exposure | PARTIAL | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | No credential field or adapter exists. Add real sensitive-field and logging tests when integration is implemented. |
| INV-13 | No strategy promotion without validation | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-14 | No retrospective performance manipulation | PARTIAL | `services/research.py`, `models/lab.py` | O05, O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Snapshot input hashes and role-level immutability exist. Add experiment parameters, amendments and prospective outcomes. |
| INV-15 | No silent synthetic-data substitution | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-16 | No ignoring material transaction costs in net returns | NOT_STARTED | — | — | — | Required when virtual execution, costs and sizing are implemented. |
| INV-17 | No invalid position sizing | NOT_STARTED | — | — | — | Required when virtual execution, costs and sizing are implemented. |
| INV-18 | No cross-company unauthorized access | COMPLETE | `security/ir.access.csv`, `models/lab.py` | O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Add regression checks for future features and independent API calls. |
| INV-19 | No risk veto overridden by signal score | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-20 | No forced daily trading recommendation | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-21 | No experimental strategy presented as validated | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-22 | No real account capital allocation | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-23 | No unbounded background processing | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | U04, P01 | `docs/evidence/performance/services.csv` | Current paths are bounded and manual. Add bounded scheduling when implemented. |
| INV-24 | No paper profit represented as real profit | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-25 | No test marked PASSED without execution evidence | COMPLETE | `DEVELOPMENT_REPORT.md` | D01 | Sections 10–15 and 22 | No financial performance or production readiness claimed. |
| INV-26 | No unsupported market data entitlement bypass | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-27 | No missing required data treated as positive evidence | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-28 | No historical signal deletion to hide losses | PARTIAL | `services/research.py`, `models/lab.py` | O05, O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Snapshot input hashes and role-level immutability exist. Add experiment parameters, amendments and prospective outcomes. |
| INV-29 | No dashboard KPI without a defined data source | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-30 | No production-readiness claim with unresolved critical blockers | COMPLETE | `DEVELOPMENT_REPORT.md` | D01 | Sections 10–15 and 22 | No financial performance or production readiness claimed. |
| S28-001 | Create traceable tests for each applicable invariant | NOT_STARTED | — | — | — | Evaluated as part of the corresponding future feature. |
| S29-001 | Implement and execute actual tests | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-002 | Indicator mathematical correctness | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-003 | Indicator warm-up | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-004 | Candle validation | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-005 | Missing values | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-006 | Numerical precision | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-007 | Strategy entry and exit rules | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-008 | Risk calculations | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-009 | Position sizing | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-010 | Trading cost calculations | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-011 | Expected value calculations | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-012 | Statistical metrics | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-013 | Probability calibration | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-014 | Look-ahead bias prevention | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-015 | Temporal feature correctness | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-016 | Fresh installation | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-017 | Module upgrade | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-018 | Model registration | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-019 | XML view validation | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-020 | Menus and actions | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-021 | Access rights | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-022 | Record rules | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-023 | Company isolation | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-024 | Scheduled actions | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-025 | Configuration persistence | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-026 | Database constraints | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-027 | Valid fixture authentication responses | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-028 | Invalid credentials | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-029 | Expired sessions | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-030 | Rate limits | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-031 | Network timeouts | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-032 | WebSocket reconnect behavior | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-033 | Invalid instrument tokens | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-034 | Historical candle response validation | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-035 | Stale quote detection | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-036 | Real API smoke tests only when authorized credentials are available | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-037 | Paper account funding | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-038 | Virtual cash reservation | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-039 | Simulated buying | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-040 | Simulated selling | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-041 | Partial execution | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-042 | Partial profit booking | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-043 | Stop-loss execution | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-044 | Trailing stop handling | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-045 | Target execution | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-046 | Intraday square-off | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-047 | Insufficient virtual cash | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-048 | Duplicate execution prevention | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-049 | Concurrent execution prevention | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-050 | Restart recovery | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-051 | Realistic slippage | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-052 | Same-candle target/stop ambiguity | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-053 | Chronological processing | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-054 | Data leakage detection | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-055 | Out-of-sample validation | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-056 | Walk-forward evaluation | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-057 | Benchmark comparison | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-058 | Insufficient sample handling | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-059 | Strategy rejection | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-060 | Strategy suspension | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-061 | Risk veto enforcement | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-062 | Signal expiration | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-063 | NO TRADE generation | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-064 | Use a real running Odoo 20 Community instance and a supported browser testing method | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-065 | Dashboard rendering | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-066 | Navigation | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-067 | KPI accuracy | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-068 | Filters | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-069 | Sorting | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-070 | Drill-downs | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-071 | Stock detail pages | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-072 | Chart rendering | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-073 | Theme behavior | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-074 | Responsive layout | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-075 | Loading states | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-076 | Empty states | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-077 | Data error states | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-078 | Stale-data alerts | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-079 | Browser console errors | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-080 | JavaScript exceptions | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-081 | RPC failures | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-082 | Capture real screenshots where possible | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-083 | Do not use generated mockup images as browser testing evidence | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-084 | RAM usage | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-085 | CPU usage | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-086 | Dashboard load time | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-087 | Historical data ingestion speed | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-088 | Research cycle duration | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-089 | Indicator computation duration | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-090 | Database query performance | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-091 | Paper simulation throughput | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-092 | Record actual hardware, dataset size, configuration, duration, and resource usage | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-093 | Internet disconnect | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-094 | Broker failure | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-095 | Invalid responses | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-096 | Missing data | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-097 | Stale data | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-098 | Database operation failure | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-099 | Research worker interruption | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-100 | Application restart | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-101 | Duplicate scheduled jobs | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-102 | Partial ingestion | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-103 | Memory pressure | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-104 | Interrupted paper-trade processing | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| S29-105 | Verify safe degradation and recovery | NOT_STARTED | — | — | — | See complete test inventory in report §10. |
| AC-001 | Odoo 20 Community compatibility verified | COMPLETE | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| AC-002 | Fresh installation successful | COMPLETE | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| AC-003 | Module upgrades safely | COMPLETE | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| AC-004 | Zero mandatory paid AI APIs | COMPLETE | `__manifest__.py`, `services/` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Runtime manifest and expanded standard-library services verified. |
| AC-005 | CPU-only operation | COMPLETE | `__manifest__.py`, `services/` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | CPU-only synthetic ORM benchmark. |
| AC-006 | 16 GB hardware optimization measured | PARTIAL | `scripts/measure_services.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | 50 instruments measured in P02. Larger workloads pending. |
| AC-007 | Secure provider configuration | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Opt-in environment configuration tested offline; account authorization pending. |
| AC-008 | Instrument master synchronization | NOT_STARTED | `models/lab.py` | — | Manual registration only | Add verified provider instrument master sync and token mapping. |
| AC-009 | Historical market data ingestion | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Calendar-aware CSV implemented, broker history verified in fixtures. |
| AC-010 | Authorized live market data integration | BLOCKED | — | B01 | Decision and sources in §08 | Verify account terms, static egress and authorized credentials. Implement a read-only adapter. |
| AC-011 | Market data freshness enforcement | PARTIAL | `services/research.py`, `models/lab.py` | O05–O06 | `docs/evidence/installation/{fresh,upgrade}.log` | NO TRADE blocks actionable historical signals. Implement live freshness or expiry gates before enabling actionable signals. |
| AC-012 | Duplicate-data prevention | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03–O04, O08 | `docs/evidence/installation/{fresh,upgrade}.log`, `docs/evidence/security/contention.log` | — |
| AC-013 | Historical data provenance | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| AC-014 | Correct indicator calculations | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | 19 causal series implemented. Full independent reference verification pending. |
| AC-015 | Research engine interface operational | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Version 2 contract implemented for three results. |
| AC-016 | Applicable research capabilities functional | PARTIAL | `services/research.py`, `models/lab.py` | U06–U08, O05–O06 | `docs/evidence/tests/unit.log` | Three descriptive findings exist. Complete the remaining indicator set, evidence contract and engine methods. |
| AC-017 | Versioned strategy framework | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | ST-01 version and code hashes; general strategy lifecycle pending. |
| AC-018 | Market regime detection | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-019 | Explainable master decision engine | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | NO TRADE with temporal and quarantine gates. Master gates pending. |
| AC-020 | Transparent quality scoring | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-021 | Risk veto enforcement | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-022 | Transaction cost calculation | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Effective-dated cost engine works with documented hypothetical tariffs. |
| AC-023 | Expected net return calculation | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Synthetic net results v1. Validated evidence and calibration remain. |
| AC-024 | Position sizing validation | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Fee-aware sizing and stop risk verified for the synthetic slice. |
| AC-025 | Signal freshness and expiry | PARTIAL | `services/research.py`, `models/lab.py` | O05–O06 | `docs/evidence/installation/{fresh,upgrade}.log` | NO TRADE blocks actionable historical signals. Implement live freshness or expiry gates before enabling actionable signals. |
| AC-026 | Historical backtesting | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Complete synthetic session replay. Authorized market and multi-session datasets pending. |
| AC-027 | Look-ahead bias prevention | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Cutoff, prefix invariance and next-opening rules tested; real data lineage pending. |
| AC-028 | Out-of-sample validation | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-029 | Walk-forward testing | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-030 | Reproducible research experiments | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Synthetic code and data hashes verified. Holdout workflow pending. |
| AC-031 | Automatic paper trading | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-032 | Virtual cash integrity | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-033 | Paper execution idempotency | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-034 | Paper portfolio reporting | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-035 | Strategy performance tracking | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-036 | Recommendation monitoring | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-037 | Automatic research scheduling | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-038 | Scheduler concurrency protection | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-039 | Premium dashboard operational | PARTIAL | `static/src/`, `views/lab.xml`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Native historical plot and company KPI additions. Full dashboards A–I incomplete. |
| AC-040 | Dashboard KPI correctness | COMPLETE | `static/src/`, `views/lab.xml`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Current overview KPI/fixture chart values verified in Edge. |
| AC-041 | Real browser UI verified | PARTIAL | `scripts/verify_browser.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Six focused real-browser checks. Full chart/filters/themes coverage incomplete. |
| AC-042 | Security permissions verified | COMPLETE | `security/ir.access.csv`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Current ACLs reverified, including calendar administration and forged research creation. |
| AC-043 | Company isolation verified | COMPLETE | `security/ir.access.csv`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Company isolation regression passed. |
| AC-044 | Credential redaction verified | PARTIAL | `__manifest__.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Credential redaction checked with offline failure fixtures. No actual credential run. |
| AC-045 | Recovery behavior verified | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Independent conflicting imports and retry verified. |
| AC-046 | No real-order functionality | COMPLETE | `__manifest__.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Mandatory prohibition verified by runtime endpoint rejection and source scan. |
| AC-047 | NO TRADE behavior verified | COMPLETE | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | NO TRADE verified in ORM and browser. |
| AC-048 | No fabricated performance results | COMPLETE | `DEVELOPMENT_REPORT.md` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Only synthetic correctness evidence reported. |
| AC-049 | Complete setup and user documentation | PARTIAL | `README.md` | D01 | README and §21 | Document setup for functionalities as they are implemented. |
| AC-050 | Evidence-backed development report generated | COMPLETE | `DEVELOPMENT_REPORT.md` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | P02 handoff and manifest verified. |
| S30-001 | Do not mark acceptance criteria as passed solely because corresponding code exists | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| S31-001 | Repository inspection | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-002 | Actual environment verification | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-003 | Requirements documentation | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-004 | Architecture | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-005 | Module foundation | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-006 | Security | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-007 | Configuration | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-008 | Data models | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-009 | Data provenance | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-010 | Hard invariants | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-011 | Market data provider foundation | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-012 | Historical data ingestion | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-013 | Data quality | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-014 | Indicator calculations | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-015 | Initial research engines | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-016 | Test infrastructure | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-017 | Strategy framework | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-018 | Risk calculations | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-019 | Cost calculations | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-020 | Master decision engine | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-021 | Backtesting foundation | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-022 | Initial paper trading | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-023 | Functional premium dashboard | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-024 | Research scanner | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-025 | Research detail views | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-026 | Paper portfolio | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-027 | Scheduler | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-028 | System health monitoring | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-029 | Additional validated strategies | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-030 | Advanced statistics | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-031 | Machine learning | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-032 | Continuous improvement | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-033 | Expanded dashboards | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-034 | Performance optimization | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-035 | Complete as much verified development as the available environment and execution budget permit | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-036 | Prioritize correctness over feature count | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-037 | Do not stop after merely writing a plan | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-038 | Do not spend the entire execution on cosmetic UI while leaving the financial and data-quality foundations incorrect | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S31-039 | Preserve all future requirements in the traceability matrix | PARTIAL | See milestone report | — | Evidence and scope in report | Continue in the priority order in the brief. |
| S32-001 | The report must include the following sections | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-002 | Product name | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-003 | Current development milestone | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-004 | Execution date | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-005 | Current Git revision | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-006 | Overall implementation status | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-007 | Current readiness decision | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-008 | Most important achievements | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-009 | Most important unresolved risks | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-010 | Operating system | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-011 | CPU model | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-012 | Available RAM | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-013 | GPU availability | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-014 | Python version | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-015 | PostgreSQL version | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-016 | Odoo version | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-017 | Odoo edition | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-018 | Repository path | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-019 | Addons path | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-020 | Relevant dependency versions | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-021 | Test database configuration, with secrets removed | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-022 | Actual directory tree | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-023 | Implemented components | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-024 | Component dependencies | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-025 | Data flow | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-026 | Research flow | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-027 | Signal lifecycle | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-028 | Paper-trade lifecycle | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-029 | Security architecture | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-030 | Architectural deviations and reasons | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-031 | Path | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-032 | Purpose | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-033 | Implementation status | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-034 | Associated requirements | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-035 | Important behavior | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-036 | Remaining limitations | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-037 | COMPLETE | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-038 | PARTIAL | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-039 | NOT_STARTED | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-040 | BLOCKED | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-041 | DEFERRED_OUT_OF_SCOPE | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-042 | Implementation status | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-043 | Mathematical method | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-044 | Required data | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-045 | Available data | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-046 | Validation status | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-047 | Test coverage | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-048 | Known limitations | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-049 | Signal eligibility | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-050 | Strategy ID | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-051 | Version | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-052 | Implementation status | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-053 | Validation status | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-054 | Historical dataset | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-055 | Training period | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-056 | Validation period | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-057 | Final holdout period | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-058 | Number of trades | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-059 | Trading cost assumptions | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-060 | Net results | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-061 | Maximum drawdown | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-062 | Limitations | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-063 | Current eligibility | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-064 | Use NOT TESTED when evidence does not exist | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-065 | Official sources consulted | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-066 | Authentication implementation | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-067 | Static IP findings | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-068 | API entitlement findings | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-069 | Rate-limit configuration | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-070 | Historical integration status | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-071 | Live integration status | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-072 | WebSocket status | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-073 | Actual live test evidence | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-074 | Mock test evidence | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-075 | Missing credentials or access blockers | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-076 | Required owner setup steps | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-077 | Never include actual secrets | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-078 | Implementation status | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-079 | Implemented KPIs | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-080 | Calculation source | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-081 | Working filters | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-082 | Working drill-downs | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-083 | Browser verification | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-084 | Screenshot evidence | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-085 | Known UI issues | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-086 | Remaining development | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-087 | Include every executed and planned test | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-088 | PASSED | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-089 | FAILED | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-090 | BLOCKED | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-091 | SKIPPED | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-092 | NOT_RUN | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-093 | Distinguish unit tests, integration tests, simulated provider tests, and real external integration tests | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-094 | Exact test commands | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-095 | Exit codes | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-096 | Test counts | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-097 | Passed counts | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-098 | Failed counts | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-099 | Skipped counts | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-100 | Execution duration | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-101 | Relevant sanitized logs | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-102 | Evidence file paths | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-103 | If a command failed, include the real failure reason and subsequent repair status | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-104 | Do not fabricate test output | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-105 | Include implementation paths, verification method, test evidence, status, and remaining work | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-106 | Every criterion must have an explicit status | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-107 | Dataset provenance | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-108 | Dataset size | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-109 | Backtesting periods | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-110 | Strategy performance | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-111 | Trading costs | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-112 | Net returns | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-113 | Profit factor | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-114 | Drawdowns | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-115 | Sample sizes | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-116 | Statistical uncertainty | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-117 | Relevant limitations | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-118 | If no valid research experiment has been completed, state that clearly | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-119 | CPU usage | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-120 | RAM usage | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-121 | Dataset sizes | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-122 | Research durations | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-123 | Ingestion durations | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-124 | Dashboard timings | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-125 | Database bottlenecks | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-126 | Hardware limitations | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-127 | Distinguish measured performance from target performance | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-128 | ACL results | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-129 | Record rule results | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-130 | Company isolation results | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-131 | Credential protection | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-132 | Secret scanning | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-133 | Unauthorized operation tests | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-134 | Real-order execution prohibition verification | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-135 | Security issues and repairs | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-136 | Bug ID | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-137 | Severity | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-138 | Root cause | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-139 | Affected components | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-140 | Fix implemented | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-141 | Regression test | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-142 | Retest result | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-143 | Remaining risk | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-144 | Requirement ID | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-145 | Current state | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-146 | Reason incomplete | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-147 | Dependencies | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-148 | Priority | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-149 | Recommended next implementation | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-150 | Foundation | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-151 | Market data | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-152 | Research engines | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-153 | Strategies | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-154 | Statistical validation | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-155 | Backtesting | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-156 | Risk management | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-157 | Paper trading | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-158 | Dashboard | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-159 | Automation | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-160 | Security | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-161 | Testing | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-162 | Documentation | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-163 | Do not guess a completion percentage | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-164 | Do not count unverified placeholders as completed features | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-165 | Critical blockers | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-166 | Required repairs | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-167 | Highest-value incomplete features | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-168 | Dependencies | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-169 | Missing tests | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-170 | Performance improvements | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-171 | Dashboard improvements | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-172 | Research improvements | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-173 | Suggested next milestone | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-174 | Exact implementation paths relevant to continuation | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-175 | Do not require the next developer to rediscover information already known | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-176 | Installing dependencies | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-177 | Starting Odoo | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-178 | Installing the module | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-179 | Configuring a paper trading account | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-180 | Connecting authorized Angel One market data | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-181 | Importing historical data | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-182 | Running research | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-183 | Opening the dashboard | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-184 | Executing relevant tests | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-185 | DEVELOPMENT INCOMPLETE | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-186 | FOUNDATION VERIFIED | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-187 | HISTORICAL RESEARCH READY | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-188 | PAPER TRADING TEST READY | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-189 | VERIFIED RESEARCH BETA | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-190 | VALIDATED RESEARCH RELEASE READY | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-191 | Do not claim live trading readiness | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S32-192 | Do not claim production-quality signal accuracy without appropriate historical, out-of-sample, and prospective paper-trading evidence | PARTIAL | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S33-001 | Store real evidence where available | COMPLETE | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S33-002 | Ensure evidence contains no passwords, API keys, TOTP secrets, private account identifiers, or authentication tokens | NOT_STARTED | — | — | — | Capture artifacts as real tests become available. |
| S33-003 | Create an evidence manifest with file paths and SHA-256 hashes where practical | COMPLETE | `DEVELOPMENT_REPORT.md` | D01 | `docs/evidence/manifest.sha256` | — |
| S34-001 | No fabricated development results | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-002 | No fabricated test results | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-003 | No fabricated API integration results | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-004 | No fabricated research performance | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-005 | No fabricated live market prices | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-006 | No fabricated historical statistics | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-007 | No hidden incomplete features | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-008 | No misleading completion percentage | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-009 | No unsupported profit guarantee | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-010 | No fake premium dashboard | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-011 | No unauthorized broker operation | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-012 | No real-money trading | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-013 | No paid AI dependency | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-014 | No unnecessary GPU dependency | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-015 | No unsafe secrets | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-016 | No ignored critical errors | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-017 | No unverified release-readiness declaration | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-018 | Resolve discovered bugs whenever possible | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-019 | After each significant repair, execute the relevant regression tests again | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S34-020 | If a test cannot be executed, report the specific blocker | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S35-001 | Do not finish with only a textual development plan | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S35-002 | Print only actual measured counts and statuses | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S35-003 | The complete DEVELOPMENT_REPORT.md will be submitted to an independent technical reviewer who will prepare the next development prompt based on the actual development state | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S35-004 | Build the strongest possible foundation | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |
| S35-005 | Prioritize mathematical correctness, trustworthy data, realistic simulations, capital protection, explainability, premium user experience, and verified engineering quality | PARTIAL | See milestone report | — | Evidence and scope in report | Preserve as an operating and quality requirement. |

| Requirement ID | Requirement | Status | Implementation | Test ID | Evidence | Remaining Work |
| --- | --- | --- | --- | --- | --- | --- |
| P02-S01-001 | Principal Odoo 20 Community architecture. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S01-002 | Financial market data engineering. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S01-003 | Quantitative trading research. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S01-004 | Mathematical and statistical correctness. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S01-005 | Python performance engineering. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S01-006 | Angel One SmartAPI integration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S01-007 | Financial risk management. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S01-008 | Historical strategy validation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S01-009 | Native OWL frontend development. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S01-010 | Professional financial dashboard design. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S01-011 | PostgreSQL integrity and concurrency. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S01-012 | Application security. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S01-013 | Automated testing. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S01-014 | Evidence-driven quality assurance. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S02-001 | `DEVELOPMENT_REPORT.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S02-002 | `docs/MASTER_REQUIREMENTS.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S02-003 | `docs/REQUIREMENTS_TRACEABILITY.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S02-004 | `docs/ARCHITECTURE.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S02-005 | `docs/DEVELOPMENT_PLAN.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S02-006 | `docs/DECISION_LOG.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S02-007 | `docs/RISK_REGISTER.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S02-008 | `README.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S02-009 | RE-01 through RE-25 research capability identifier. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S02-010 | ST-01 through ST-20 strategy identifier. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S02-011 | INV-01 through INV-30 business invariant. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S02-012 | AC-001 through AC-050 acceptance criterion. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S02-013 | Existing S-series traceability identifier. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S02-014 | Previously implemented and verified behavior. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S03-001 | Readiness: FOUNDATION VERIFIED for the historical descriptive research slice. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S03-002 | Applicable requirements: 1,236. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S03-003 | Complete requirements: 72. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S03-004 | Requirements coverage: approximately 5.83%. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S03-005 | Acceptance criteria passed: 14 of 50. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S03-006 | Named test inventory: 24 PASSED, 0 FAILED, 1 BLOCKED, 70 NOT_RUN and 29 grouped coverage references. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S03-007 | Research engines: RE-01, RE-05 and RE-18 partially implemented. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S03-008 | Other research engines: not started. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S03-009 | Trading strategies: none implemented. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S03-010 | Financial research experiments: none completed. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S03-011 | Existing decision output: historical NO TRADE. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S03-012 | Broker adapter: not implemented. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S03-013 | Paper trading: not implemented. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S03-014 | Dashboard: initial OWL overview and native record views. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-001 | Windows NT 10.0.26300.0. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-002 | Intel Core i5-10210U. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-003 | Four physical CPU cores. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-004 | Eight logical processors. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-005 | Approximately 16 GB RAM. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-006 | Approximately 3.4 GiB available RAM at inspection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-007 | Intel UHD integrated graphics. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-008 | No dedicated GPU. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-009 | Python 3.14.6 in the Odoo virtual environment. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-010 | PostgreSQL 18.4. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-011 | Odoo 20 Community. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-012 | Module path: `C:/PycharmProjects/odoo20/custom_addons/golok_ai_trading_lab_pro`. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-013 | Paid AI APIs. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-014 | Local LLMs. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-015 | Ollama. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-016 | GPU acceleration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-017 | Paid cloud computing. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S04-018 | Mandatory paid analytics subscriptions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S05-001 | Real order placement. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S05-002 | Real order modification. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S05-003 | Real order cancellation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S05-004 | Automatic real-money buying. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S05-005 | Automatic real-money selling. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S05-006 | Automatic allocation of real account balances. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S05-007 | Fund transfer functionality. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S05-008 | Hidden real-order execution services. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S05-009 | Dormant autonomous trading code. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-001 | Inspect the complete module source. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-002 | Inspect all existing database models and constraints. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-003 | Verify existing security groups and company domains. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-004 | Review every existing public RPC-callable method. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-005 | Inspect the previous evidence manifest. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-006 | Verify referenced evidence paths and hashes. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-007 | Inspect historical failure logs and subsequent repairs. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-008 | Re-execute the previous standalone tests. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-009 | Re-execute the Odoo integration tests. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-010 | Re-execute the independent database contention test. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-011 | Re-execute the real browser test suite. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-012 | Identify regressions and hidden incomplete implementations. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-013 | Repair confirmed defects before building dependent features. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-014 | BUG-01: Odoo 20 `ir.access` migration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-015 | BUG-02: Odoo 20 BinaryValue handling. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-016 | BUG-03: Sass compatibility. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-017 | BUG-04: OWL 3 reactivity and template scope. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S06-018 | ENV-01: Isolated PostgreSQL harness execution. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S07-001 | Create a non-destructive source baseline manifest with SHA-256 hashes. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S07-002 | Establish a recoverable local source checkpoint. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S07-003 | Exclude credentials, test database contents, virtual environments, runtime logs and private market data. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S07-004 | Document an appropriate version-control setup. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-001 | Place real broker orders — COMPLETE. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-002 | Modify real broker orders — COMPLETE. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-003 | Automatically buy real shares — COMPLETE. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-004 | Real broker order placement is prohibited and absent. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-005 | Real broker order modification is prohibited and absent. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-006 | Automatic real-money buying is prohibited and absent. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-007 | A working verified capability. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-008 | A partially implemented capability. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-009 | A mandatory prohibition. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-010 | An unavailable external dependency. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-011 | An optional technology. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-012 | A future out-of-scope feature. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-013 | A guard that currently holds only because the underlying feature does not exist. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-014 | Functional capability coverage. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-015 | Mandatory constraint compliance. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-016 | Acceptance criteria verification. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-017 | Test execution coverage. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-018 | External integration verification. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S08-019 | Financial strategy validation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-001 | Exchange identifiers. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-002 | Trading dates. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-003 | Standard trading sessions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-004 | Pre-open session distinctions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-005 | Market holidays. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-006 | Weekends. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-007 | Special trading sessions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-008 | Session opening and closing timestamps. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-009 | Intraday entry cutoff configuration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-010 | Intraday exit cutoff configuration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-011 | Session versioning. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-012 | Calendar source provenance. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-013 | Calendar verification date. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-014 | Asia/Kolkata display semantics. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-015 | UTC storage semantics. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-016 | Candles outside authorized sessions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-017 | Candles spanning invalid session boundaries. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-018 | Future-dated closed candles. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-019 | Research from incomplete candles. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-020 | Incorrect aggregation across overnight boundaries. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-021 | Incorrect daily candle assignment. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-022 | Incorrect holiday gap classification. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-023 | Market event time. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-024 | Candle opening time. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-025 | Candle closing time. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-026 | Source publication or availability time. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-027 | Application ingestion time. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S09-028 | Research decision time. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-001 | Exchange. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-002 | Trading symbol. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-003 | Provider-specific token mapping. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-004 | ISIN where available. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-005 | Instrument type. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-006 | Trading segment. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-007 | Tick size. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-008 | Lot size. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-009 | Listing status. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-010 | Effective date. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-011 | Suspension status. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-012 | Delisting status. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-013 | Sector classification. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-014 | Reference data source. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-015 | Mapping version. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S10-016 | Mapping verification state. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-001 | Decimal price precision. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-002 | Immutable candle records. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-003 | Existing conflict detection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-004 | Existing idempotent import behavior. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-005 | Historical research snapshot digests. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-006 | Company isolation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-007 | Explicit source classifications. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-008 | Historical versus live data classification. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-009 | Delayed data classification. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-010 | Synthetic fixture classification. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-011 | Dataset authorization status. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-012 | Source verification status. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-013 | Session-aware missing candle detection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-014 | Candle completeness checks. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-015 | Data freshness checks. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-016 | Quote age checks. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-017 | Sequence or timestamp ordering checks. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-018 | Provider schema validation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-019 | Data quality issue records. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-020 | Dataset quarantine. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-021 | Provider outage detection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-022 | Controlled recovery. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-023 | Structurally valid data. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-024 | Calendar-valid data. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-025 | Source-verified data. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-026 | Point-in-time eligible data. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-027 | Research-only data. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S11-028 | Live decision-eligible data. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-001 | https://smartapi.angelone.in/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-002 | https://smartapi.angelone.in/docs | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-003 | https://github.com/angel-one/smartapi-python | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-004 | Account-specific pricing. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-005 | Market data entitlements. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-006 | Static IP requirements. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-007 | Personal use restrictions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-008 | Data storage and redistribution restrictions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-009 | Authentication requirements. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-010 | Session expiration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-011 | REST rate limits. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-012 | WebSocket limits. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-013 | Historical lookback limits. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-014 | Supported instrument types. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-015 | Protected provider configuration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-016 | Authentication. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-017 | Session lifecycle. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-018 | Controlled reauthentication. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-019 | Instrument master synchronization. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-020 | Historical candle retrieval. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-021 | Live quote retrieval. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-022 | Read-only WebSocket subscriptions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-023 | Heartbeat monitoring. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-024 | Connection state management. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-025 | Exponential backoff. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-026 | Bounded retries. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-027 | Timeout handling. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-028 | Rate-limit enforcement. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-029 | Schema error handling. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-030 | Connectivity diagnostics. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-031 | Last successful request tracking. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-032 | Subscription count monitoring. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-033 | Data lag tracking. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-034 | Database-readable configuration fields. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-035 | Browser responses. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-036 | HTTP diagnostics. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-037 | Screenshots. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-038 | Test artifacts. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-039 | Source code. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-040 | Exceptions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-041 | Development reports. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-042 | Implement and execute deterministic fixture integration tests. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-043 | Keep real network integration disabled. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-044 | Mark live smoke tests BLOCKED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S12-045 | Continue developing independent functionality. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-001 | NOT_CONFIGURED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-002 | AUTH_REQUIRED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-003 | CONNECTING. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-004 | CONNECTED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-005 | DEGRADED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-006 | RATE_LIMITED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-007 | STALE. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-008 | DISCONNECTED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-009 | BLOCKED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-010 | ERROR. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-011 | Block new actionable recommendations. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-012 | Invalidate affected recommendations where applicable. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-013 | Stop generating simulated fills from stale prices. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-014 | Preserve existing records. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-015 | Allow authorized historical research to continue independently. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S13-016 | Clearly display the failure on the dashboard. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-001 | SMA. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-002 | EMA. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-003 | RSI. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-004 | MACD. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-005 | ATR. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-006 | VWAP. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-007 | ADX. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-008 | Bollinger Bands. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-009 | Stochastic Oscillator. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-010 | Relative Volume. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-011 | Rate of Change. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-012 | On-Balance Volume. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-013 | Historical Volatility. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-014 | Rolling Highs and Lows. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-015 | Opening Range. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-016 | Relative Strength. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-017 | Price Gaps. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-018 | Volume Spikes. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-019 | Trend Slopes. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-020 | Mathematical formula. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-021 | Algorithm version. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-022 | Input requirements. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-023 | Warm-up period. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-024 | Null and missing-value policy. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-025 | Numerical precision. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-026 | Timeframe semantics. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-027 | Session behavior. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-028 | Expected output. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-029 | Invalid-input behavior. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-030 | VWAP resets per applicable session. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-031 | Opening range cannot be known before its configured window closes. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-032 | Breakout levels must exclude future bars. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-033 | Relative volume must use a documented baseline. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-034 | Relative strength requires a properly aligned benchmark. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-035 | Rolling statistics must not include future observations. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-036 | Zero-volume and zero-denominator cases must be handled explicitly. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-037 | ATR and RSI smoothing must match documented conventions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-038 | Standard deviation conventions must be declared. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S14-039 | Warm-up values must remain unavailable rather than silently defaulting to zero. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-001 | Engine ID. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-002 | Engine version. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-003 | Instrument. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-004 | Dataset identity. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-005 | Research timestamp. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-006 | Decision cutoff. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-007 | Required input fields. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-008 | Data source and freshness. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-009 | Findings. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-010 | Supporting evidence. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-011 | Contradictory evidence. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-012 | Missing inputs. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-013 | Limitations. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-014 | Applicable strategies. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-015 | Execution duration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-016 | Result status. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-017 | Input digest. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-018 | COMPLETED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-019 | NOT_APPLICABLE. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-020 | INSUFFICIENT_DATA. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-021 | STALE_DATA. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-022 | ERROR. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-023 | RE-01 Technical Analysis. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-024 | RE-03 Price Action. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-025 | RE-04 Candlestick Patterns. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-026 | RE-05 Volume Intelligence. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-027 | RE-06 Support and Resistance. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-028 | RE-07 Breakout Detection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-029 | RE-08 False Breakout Detection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-030 | RE-09 Market Trend. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-031 | RE-15 Historical Patterns. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-032 | RE-17 Liquidity Analysis, explicitly limited to available proxies. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-033 | RE-18 Volatility. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-034 | RE-19 Momentum. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S15-035 | RE-20 Abnormal Market Activity. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-001 | Brokerage. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-002 | Securities Transaction Tax. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-003 | Exchange transaction charges. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-004 | Applicable SEBI charges. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-005 | GST. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-006 | Stamp duty. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-007 | Bid-ask spread. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-008 | Slippage. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-009 | Other verified applicable charges. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-010 | Effective start date. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-011 | Effective end date when applicable. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-012 | Exchange. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-013 | Trading segment. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-014 | Transaction side. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-015 | Charge basis. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-016 | Rate or fixed amount. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-017 | Minimum or maximum charge if applicable. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-018 | Rounding method. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-019 | Official source. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-020 | Verification status. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-021 | Gross trading P&L. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-022 | Brokerage. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-023 | Statutory charges. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-024 | Execution friction. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-025 | Net trading P&L. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-026 | Small trades. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-027 | Large trades. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-028 | Different buy/sell charges. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-029 | Tariff effective-date boundaries. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-030 | Rounding. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-031 | Zero and invalid quantities. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-032 | Missing tariff information. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S16-033 | Negative net profit despite positive gross profit. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-001 | Virtual reference capital: INR 50,000. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-002 | Planned per-trade risk: 0.5%. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-003 | Planned daily loss threshold: 1%. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-004 | Minimum net planned reward-to-risk ratio: 2:1. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-005 | Preferred candidate reward-to-risk: 3:1. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-006 | Maximum daily paper entries: 3. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-007 | Consecutive loss pause threshold: 2. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-008 | No leverage. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-009 | No averaging losing positions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-010 | No martingale. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-011 | No short strategy activation at this milestone. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-012 | Capital-aware position sizing. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-013 | Fee-aware position sizing. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-014 | Stop-loss validation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-015 | Target validation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-016 | Tick-size validation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-017 | Quantity validation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-018 | Liquidity-based sizing restrictions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-019 | Maximum planned risk validation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-020 | Estimated adverse execution allowance. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-021 | Minimum net reward-to-risk validation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-022 | Independent risk veto. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S17-023 | Structured risk rejection reasons. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-001 | Strategy ID. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-002 | Version. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-003 | Code or implementation digest. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-004 | Parameter configuration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-005 | Applicable market regime. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-006 | Required indicators. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-007 | Required data. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-008 | Entry conditions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-009 | Exit conditions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-010 | Stop methodology. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-011 | Target methodology. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-012 | Risk policy. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-013 | Expiry policy. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-014 | Research validation state. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-015 | DRAFT. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-016 | RESEARCH_ONLY. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-017 | BACKTESTED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-018 | VALIDATION_FAILED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-019 | VALIDATION_BLOCKED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-020 | PAPER_EVALUATION. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S18-021 | SUSPENDED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-001 | Opening range duration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-002 | Eligible trading session. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-003 | Breakout confirmation method. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-004 | Volume confirmation method. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-005 | Optional trend confirmation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-006 | Maximum acceptable entry deviation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-007 | Entry cutoff. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-008 | Stop-loss methodology. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-009 | Target methodology. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-010 | Maximum holding period. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-011 | Session exit policy. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-012 | False-breakout invalidation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-013 | Risk restrictions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-014 | Cost restrictions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-015 | Qualifying breakout. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-016 | Unconfirmed breakout. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-017 | Insufficient opening range data. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-018 | Low-volume rejection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-019 | Excessive volatility rejection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-020 | Late-session rejection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-021 | Invalid data rejection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-022 | Risk rejection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-023 | Cost rejection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S19-024 | Expired candidate rejection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-001 | Load an explicitly identified dataset. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-002 | Validate dataset eligibility. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-003 | Iterate observations chronologically. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-004 | Generate a decision using available information. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-005 | Simulate entry only after decision availability. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-006 | Apply capital and risk checks. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-007 | Apply realistic execution assumptions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-008 | Monitor stop and target conditions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-009 | Close simulated positions according to policy. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-010 | Record gross and net outcomes. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-011 | Calculate reproducible experiment results. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-012 | Price gaps through stops. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-013 | Gap openings beyond target prices. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-014 | Same-candle target/stop ambiguity. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-015 | Entry and exit ambiguity. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-016 | Missing market data. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-017 | Incomplete candles. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-018 | Illiquid observations. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-019 | Suspended instruments. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-020 | Session closing. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-021 | Insufficient capital. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-022 | Transaction costs. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S20-023 | Slippage. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-001 | Total simulated trades. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-002 | Winning trades. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-003 | Losing trades. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-004 | Neutral trades. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-005 | Gross profit. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-006 | Gross loss. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-007 | Total costs. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-008 | Net P&L. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-009 | Average net trade. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-010 | Win rate. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-011 | Profit factor. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-012 | Maximum drawdown. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-013 | Equity curve. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-014 | Consecutive losses. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-015 | Net expectancy. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-016 | Maximum adverse excursion where supported. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S21-017 | Maximum favorable excursion where supported. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-001 | Dataset identifiers and hashes. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-002 | Universe selection rules. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-003 | Strategy version. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-004 | Parameter configuration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-005 | Cost schedule. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-006 | Risk configuration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-007 | Execution model. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-008 | Training period. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-009 | Validation period. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-010 | Final holdout period. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-011 | Benchmark. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-012 | Predeclared performance acceptance rules. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-013 | Random splitting that leaks future market information. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-014 | Parameter tuning on the final holdout. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-015 | Survivorship bias misrepresentation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-016 | Corporate action contamination. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-017 | Repeated holdout selection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-018 | Selective omission of failed experiments. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-019 | Execute deterministic synthetic correctness tests. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-020 | Mark financial validation as BLOCKED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S22-021 | Do not publish win-rate or profitability claims. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-001 | G01: Source eligibility. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-002 | G02: Instrument eligibility. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-003 | G03: Trading session validity. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-004 | G04: Candle completeness. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-005 | G05: Market data freshness. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-006 | G06: Research input sufficiency. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-007 | G07: Strategy implementation status. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-008 | G08: Strategy validation status. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-009 | G09: Cost model availability. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-010 | G10: Position sizing. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-011 | G11: Independent risk veto. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-012 | G12: Decision expiry. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-013 | G13: Evidence integrity. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-014 | G14: Research-mode restrictions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-015 | Historical descriptive results. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-016 | WATCH observations. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-017 | RESEARCH CANDIDATE results. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-018 | BACKTEST CANDIDATE results. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-019 | Explicit simulation candidates. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-020 | NO TRADE. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-021 | INVALIDATED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S23-022 | EXPIRED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-001 | Virtual account creation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-002 | Opening balance. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-003 | Available cash. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-004 | Reserved virtual cash. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-005 | Simulated order lifecycle. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-006 | Simulated fill lifecycle. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-007 | Long virtual positions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-008 | Closed virtual positions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-009 | Transaction costs. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-010 | Realized virtual P&L. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-011 | Unrealized virtual P&L. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-012 | Immutable virtual ledger events. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-013 | Trading journal. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-014 | Available cash cannot become negative. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-015 | Reserved cash cannot become negative. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-016 | Filled quantity cannot exceed permitted quantity. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-017 | Closed quantity cannot exceed open quantity. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-018 | Duplicate fills cannot change balances twice. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-019 | The virtual ledger must reconcile with cash, positions and realized P&L. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-020 | All material balance changes must be auditable. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S24-021 | Failed database transactions must not leave partial state. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-001 | Clean professional typography. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-002 | Compact financial KPI cards. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-003 | Consistent spacing and alignment. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-004 | Responsive desktop and mobile layout. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-005 | Professional light and dark theme compatibility. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-006 | Subtle neutral surfaces. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-007 | Blue accent for research and navigation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-008 | Green and red for actual positive and negative financial outcomes. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-009 | Amber for uncertainty, staleness and warnings. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-010 | Accessible status labels. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-011 | Clear data timestamps. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-012 | Fast and bounded chart rendering. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-013 | Golok AI Trading Lab Pro. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-014 | Current company. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-015 | Current research mode. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-016 | Market session state. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-017 | Market data provider state. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-018 | Last successful update. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-019 | Data freshness. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-020 | Research readiness state. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-021 | Registered instruments. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-022 | Eligible instruments. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-023 | Active datasets. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-024 | Stored candles. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-025 | Validated candles. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-026 | Quarantined datasets. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-027 | Data quality issues. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-028 | Missing observations. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-029 | Provider connectivity. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-030 | Last ingestion time. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-031 | Searchable stock table. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-032 | Exchange filter. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-033 | Dataset filter. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-034 | Research state filter. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-035 | Timeframe filter. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-036 | Data quality filter. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-037 | Strategy candidate filter. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-038 | Last research timestamp. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-039 | Research duration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-040 | Rejection reasons. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-041 | OHLC candlestick chart. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-042 | Volume chart. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-043 | Available SMA and EMA overlays. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-044 | VWAP overlay when applicable. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-045 | Opening range visualization. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-046 | Support and resistance observations where implemented. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-047 | Indicator values. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-048 | Research result cards. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-049 | Supporting and contradictory evidence. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-050 | Data quality information. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-051 | Historical decision cutoff. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-052 | Dataset provenance. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-053 | Registered strategy versions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-054 | Implemented strategies. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-055 | Research-only status. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-056 | Backtest experiments. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-057 | Validation status. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-058 | Sample sizes. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-059 | Dataset provenance. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-060 | Net experiment results. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-061 | Drawdown. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-062 | Costs. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-063 | Rejection reasons. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-064 | Virtual starting capital. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-065 | Available virtual cash. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-066 | Reserved virtual cash. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-067 | Open virtual positions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-068 | Virtual equity. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-069 | Realized virtual P&L. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-070 | Unrealized virtual P&L. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-071 | Trade history. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-072 | Provider connection state. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-073 | Last successful synchronization. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-074 | API error state. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-075 | Data lag. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-076 | Research job state. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-077 | CPU usage. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-078 | RAM usage. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-079 | Storage usage. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-080 | Last research duration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-081 | Data quality. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-082 | Provider integration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-083 | Research engines. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-084 | Cost engine. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-085 | Risk engine. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-086 | Backtesting. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-087 | Paper trading. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-088 | Security. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S25-089 | Real-market recommendation eligibility. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-001 | Bounded dataset reads. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-002 | Chunked ingestion. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-003 | Bounded indicator windows. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-004 | Efficient indexes. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-005 | Configurable batch sizes. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-006 | Limited worker concurrency. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-007 | Bounded caching. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-008 | Research timeouts. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-009 | Memory-pressure checks. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-010 | Safe job cancellation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-011 | Persistent checkpoints where scheduling is implemented. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-012 | Number of instruments. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-013 | Candles per instrument. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-014 | Dataset size. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-015 | Database operations. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-016 | Query latency. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-017 | Total research duration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-018 | Process memory. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-019 | System memory. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-020 | CPU utilization. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S26-021 | Browser response latency. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-001 | Unique job identity. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-002 | Job type. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-003 | Company scope. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-004 | Requested timestamp. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-005 | Execution status. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-006 | Start and completion timestamps. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-007 | Retry count. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-008 | Failure reason. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-009 | Checkpoint. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-010 | Maximum runtime. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-011 | Cancellation state. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-012 | Database-backed duplicate prevention. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-013 | Independent transaction locking. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-014 | Bounded job execution. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-015 | Recovery of interrupted jobs. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S27-016 | Controlled retry policy. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-001 | Trading Research Viewer. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-002 | Trading Research Analyst. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-003 | Trading Risk Manager. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-004 | Trading System Administrator. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-005 | Unauthorized model creation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-006 | Unauthorized record modification. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-007 | Unauthorized record deletion. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-008 | Cross-company relational references. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-009 | Company switching. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-010 | Forged RPC arguments. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-011 | Direct API calls. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-012 | Unauthorized dashboard data access. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-013 | Unauthorized provider configuration. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-014 | Credential redaction. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-015 | Unauthorized dataset import. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-016 | Unauthorized research execution. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-017 | Immutable historical record protection. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-018 | Virtual ledger manipulation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S28-019 | Strategy status manipulation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S30-001 | Fresh module installation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S30-002 | Same-version upgrade. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S30-003 | Upgrade from the preserved P01 source baseline. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S30-004 | Upgrade of a populated P01 test database. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S30-005 | Data retention checks. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S30-006 | XML ID retention checks. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S30-007 | Immutable snapshot retention checks. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-001 | Audit. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-002 | Baseline regression. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-003 | Traceability correction. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-004 | Evidence integrity. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-005 | Security preservation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-006 | Exchange calendar. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-007 | Reference data. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-008 | Point-in-time data. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-009 | Market data quality. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-010 | Read-only provider foundation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-011 | Indicator library. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-012 | Research engine contract. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-013 | Cost engine. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-014 | Independent risk calculations. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-015 | ST-01. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-016 | Historical backtesting. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-017 | Financial research metrics. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-018 | Validation infrastructure. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-019 | Initial virtual ledger. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-020 | Background jobs. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S31-021 | Expanded research capabilities. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-001 | `README.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-002 | `docs/MASTER_REQUIREMENTS.md` only through clearly identified additions, preserving the original requirements. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-003 | `docs/ARCHITECTURE.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-004 | `docs/REQUIREMENTS_TRACEABILITY.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-005 | `docs/DEVELOPMENT_PLAN.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-006 | `docs/DECISION_LOG.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-007 | `docs/RISK_REGISTER.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-008 | `docs/MARKET_DATA_SOURCES.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-009 | `docs/SMARTAPI_SETUP.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-010 | `docs/EXCHANGE_CALENDAR.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-011 | `docs/INDICATOR_FORMULAS.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-012 | `docs/STRATEGY_SPECIFICATIONS.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-013 | `docs/TRANSACTION_COST_MODEL.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-014 | `docs/RISK_POLICY.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-015 | `docs/BACKTEST_EXECUTION_POLICY.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-016 | `docs/DASHBOARD_KPI_DEFINITIONS.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-017 | `docs/PAPER_LEDGER_INVARIANTS.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S32-018 | `docs/VALIDATION_PROTOCOL.md` | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-001 | baseline/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-002 | installation/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-003 | upgrade/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-004 | unit/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-005 | integration/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-006 | provider/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-007 | calendar/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-008 | quantitative/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-009 | financial/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-010 | backtesting/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-011 | paper/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-012 | browser/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-013 | screenshots/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-014 | concurrency/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-015 | performance/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-016 | security/ | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-017 | Exact commands. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-018 | Exit codes. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-019 | Raw sanitized logs. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-020 | Test runner counts. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-021 | Execution durations. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-022 | Environment versions. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-023 | Dataset identities. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-024 | Actual browser screenshots. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-025 | Financial calculation fixtures. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-026 | Reconciliation results. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-027 | Measured performance. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S33-028 | Concurrency evidence. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-001 | P01 baseline. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-002 | P02 actual results. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-003 | Newly implemented capabilities. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-004 | Preserved capabilities. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-005 | Regressions detected. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-006 | Regressions repaired. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-007 | Remaining blockers. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-008 | Requirement ID. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-009 | File path. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-010 | Previous behavior. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-011 | New behavior. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-012 | Implementation status. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-013 | Test evidence. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-014 | Remaining limitation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-015 | Adapter implementation. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-016 | Fixture integration verification. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-017 | Authorized historical data verification. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-018 | Authorized live quote verification. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-019 | WebSocket verification. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-020 | Account entitlement. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-021 | Static IP requirements. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-022 | Remaining owner setup. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-023 | Synthetic correctness tests. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-024 | Historical financial experiments. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-025 | Out-of-sample experiments. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-026 | Walk-forward experiments. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-027 | Prospective paper trading. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-028 | PASSED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-029 | FAILED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-030 | BLOCKED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-031 | SKIPPED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-032 | NOT_RUN. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-033 | AC-001 through AC-050. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-034 | Comparable original requirement coverage. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-035 | Functional implementation coverage. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-036 | Acceptance verification coverage. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-037 | Executed test counts. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-038 | Research engine implementation counts. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-039 | Strategy implementation counts. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-040 | Strategy validation counts. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-041 | Dashboard implementation status. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-042 | Critical blockers. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-043 | High-priority incomplete features. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-044 | Required repairs. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-045 | External dependencies. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-046 | Exact source paths. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-047 | Missing test evidence. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-048 | Performance bottlenecks. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S34-049 | Recommended next milestone. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S35-001 | DEVELOPMENT INCOMPLETE. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S35-002 | FOUNDATION VERIFIED. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S35-003 | HISTORICAL RESEARCH READY. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S35-004 | PAPER TRADING TEST READY. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S35-005 | VERIFIED RESEARCH BETA. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |
| P02-S35-006 | VALIDATED RESEARCH RELEASE READY. | TRACKED | See corresponding P02 acceptance and gap sections | — | — | Line-level status roll-up is documented by P02 acceptance. |

## 06 — Research engine status

Calendar-bound runs add V2 evidence metadata for RE-01, RE-05 and RE-18. Indicator implementation does not promote any engine to market eligibility. RE-02–RE-25 other than these three remain outside the P02 ORM framework.

| Engine | Name | Status | Method | Required inputs | Available inputs | Verification | Limitations | Signal eligibility |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RE-01 | Technical Analysis | PARTIAL | 20-bar simple moving average | Validated OHLCV | CSV OHLCV | P01 checks and P02 indicator/cutoff regression | Descriptive single-window method only | Ineligible |
| RE-02 | Fundamental Analysis | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-03 | Price Action Analysis | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-04 | Candlestick Pattern Analysis | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-05 | Volume Intelligence | PARTIAL | Current volume / preceding 20-bar mean | Validated OHLCV | CSV OHLCV | P01 checks and P02 indicator/cutoff regression | Descriptive single-window method only | Ineligible |
| RE-06 | Support and Resistance | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-07 | Breakout Detection | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-08 | False Breakout Detection | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-09 | Market Trend Analysis | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-10 | Sector Performance and Rotation | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-11 | Benchmark Index Analysis | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-12 | Global Market Context | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-13 | Financial News and Event Analysis | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-14 | Institutional Activity Proxies | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-15 | Historical Pattern Analysis | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-16 | Statistical Probability Estimation | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-17 | Liquidity Analysis | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-18 | Volatility Analysis | PARTIAL | Wilder ATR(14), seeded with 14 true ranges | Validated OHLCV | CSV OHLCV | P01 checks and P02 indicator/cutoff regression | Descriptive single-window method only | Ineligible |
| RE-19 | Momentum Analysis | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-20 | Abnormal Market Activity Detection | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-21 | Entry Optimization | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-22 | Stop-Loss Optimization | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-23 | Profit Target Optimization | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-24 | Historical Strategy Performance | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |
| RE-25 | Net Expected Profit and Risk Validation | NOT_STARTED | NOT TESTED | Pending method design | — | NOT TESTED | Implementation pending | Ineligible |

## 07 — Strategy status

| Strategy | Name | Version | Implementation | Validation | Dataset and train/validation/holdout | Trade count | Cost assumptions | Net results and drawdown | Limitations and eligibility |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ST-01 | Opening Range Breakout | 1 | Synthetic replay | Financial validation BLOCKED | 9 synthetic 5-minute bars | One synthetic test trade | Hypothetical per-side schedule | Fixture correctness only | Ineligible for real market. |
| ST-02 | VWAP Pullback | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-03 | VWAP Reclaim | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-04 | Trend Following | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-05 | Momentum Continuation | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-06 | Volume Confirmed Breakout | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-07 | Support and Resistance Breakout | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-08 | Mean Reversion | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-09 | Gap Continuation | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-10 | Gap Reversal | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-11 | Multi-Timeframe Trend Confirmation | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-12 | Relative Strength Momentum | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-13 | Sector Rotation | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-14 | Volatility Compression Breakout | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-15 | Trend Pullback | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-16 | False Breakout Reversal | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-17 | Statistical Reversion | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-18 | ATR-Based Channel Breakout | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-19 | Momentum Exhaustion | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |
| ST-20 | Market Regime Adaptive Strategy | — | NOT_STARTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Pending strategy and validation. Ineligible. |

## 08 — SmartAPI integration status

Three fixture tests verify the disabled default transport and endpoint restrictions, fixture authentication/history/quote, rate limiting, credential-related errors and timeout sanitation. Authorization, static IP and data entitlement are unknown for the owner's account. Authenticated historical verification, live quotes and WebSocket verification were not executed. The adapter remains outside Odoo, has no instrument master sync or streaming, exposes no order routes and will not convert a receipt timestamp into quote freshness. Official documentation recheck and operating controls are in [SmartAPI setup](docs/SMARTAPI_SETUP.md).

## 09 — Dashboard development status

| Original area | P02 state |
|---|---|
| A Market Overview | Company, ingestion timestamp, instruments, datasets, candles, snapshots and quarantine count. No index, sector or breadth feed. |
| B Research Scanner | Native lists and history retained. A standalone stock scanner is pending. |
| C Best Opportunities | Historical NO TRADE and snapshot evidence. Actionable market candidates excluded. |
| D Stock Research Terminal | Latest snapshot OHLC and volume validated against the fixture in Edge. Indicator overlays and instrument terminal controls are pending. |
| E Paper Portfolio | No ledger or simulated balance tiles. |
| F Strategy Intelligence | Synthetic result available via CLI, with no dashboard experiment view. |
| G Risk Control Center | Fee-aware risk veto in service. No live exposure view. |
| H System Health | Offline mode and last local ingestion. Broker or scheduler metrics pending. |
| I Daily Research Report | Daily aggregation pending. |

Six Edge checks cover load, upload, chart values, research drill-down, mobile layout and failed RPC recovery. KPI definitions and visual evidence are available. [KPI definitions](docs/DASHBOARD_KPI_DEFINITIONS.md) · [Desktop](docs/evidence/p02/screenshots/overview-desktop.png) · [Mobile](docs/evidence/p02/screenshots/overview-mobile.png)

## 10 — Complete test inventory

67 executed, 67 passed, 0 failed, 2 blocked, 0 skipped, 8 planned groups not run. Group labels below can summarize several independently executed cases. The final totals count each executed unit/ORM/browser check separately, plus one per scripted scenario. Earlier infrastructure failures are tracked in section 17 and retained in the logs. Planned groups are listed without adding them to executed counts.

| Test ID | Category | Case | Final status | P02 evidence or blocker |
| --- | --- | --- | --- | --- |
| U01 | Python unit | test_duplicate_and_reversed_csv | PASSED | unit/python.log |
| U02 | Python unit | test_empty_and_size_limits | PASSED | unit/python.log |
| U03 | Python unit | test_gap_count_and_date_boundary | PASSED | unit/python.log |
| U04 | Python unit | test_invalid_prices_volume_and_timestamps | PASSED | unit/python.log |
| U05 | Python unit | test_utc_normalization_and_exact_prices | PASSED | unit/python.log |
| U06 | Python unit | test_atr_gaps_wilder_smoothing | PASSED | unit/python.log |
| U07 | Python unit | test_reference_values_and_relative_volume_baseline | PASSED | unit/python.log |
| U08 | Python unit | test_warmup_and_no_future_access | PASSED | unit/python.log |
| U09 | Python unit | test_calendar_and_time_availability | PASSED | unit/python.log |
| U10 | Python unit | test_temporal_csv_rejects_early_availability_and_future | PASSED | unit/python.log |
| U11 | Python unit | test_reference_values_and_all_prefixes | PASSED | unit/python.log |
| U12 | Python unit | test_session_reset_and_opening_range | PASSED | unit/python.log |
| U13 | Python unit | test_disabled_transport_and_endpoint_scope | PASSED | unit/python.log |
| U14 | Python unit | test_fixture_auth_history_quote_and_rate_limit | PASSED | unit/python.log |
| U15 | Python unit | test_timeout_sanitizes_transport_error | PASSED | unit/python.log |
| U16 | Python unit | test_token_reuse_and_ineligible_mapping | PASSED | unit/python.log |
| U17 | Python unit | test_breakout_reproducibility_and_stop_first | PASSED | unit/python.log |
| U18 | Python unit | test_tariffs_effective_date_and_risk | PASSED | unit/python.log |
| ORM01F | Odoo fresh | test_database_duplicate_constraint | PASSED | installation/fresh.log |
| ORM02F | Odoo fresh | test_gap_disables_findings | PASSED | installation/fresh.log |
| ORM03F | Odoo fresh | test_import_retry_and_atomic_conflict | PASSED | installation/fresh.log |
| ORM04F | Odoo fresh | test_permissions_and_company_scope | PASSED | installation/fresh.log |
| ORM05F | Odoo fresh | test_point_in_time_calendar_quarantine_and_chart | PASSED | installation/fresh.log |
| ORM06F | Odoo fresh | test_research_cutoff_evidence_and_no_trade | PASSED | installation/fresh.log |
| ORM01U | Odoo upgrade | test_database_duplicate_constraint | PASSED | installation/upgrade.log |
| ORM02U | Odoo upgrade | test_gap_disables_findings | PASSED | installation/upgrade.log |
| ORM03U | Odoo upgrade | test_import_retry_and_atomic_conflict | PASSED | installation/upgrade.log |
| ORM04U | Odoo upgrade | test_permissions_and_company_scope | PASSED | installation/upgrade.log |
| ORM05U | Odoo upgrade | test_point_in_time_calendar_quarantine_and_chart | PASSED | installation/upgrade.log |
| ORM06U | Odoo upgrade | test_research_cutoff_evidence_and_no_trade | PASSED | installation/upgrade.log |
| B01 | Real Edge | authenticated OWL dashboard and empty state | PASSED | browser/edge.log |
| B02 | Real Edge | CSV selected and imported through the Odoo wizard | PASSED | browser/edge.log |
| B03 | Real Edge | database-backed OHLC and volume matched the uploaded fixture | PASSED | browser/edge.log |
| B04 | Real Edge | historical research, accurate KPIs, refresh and snapshot drill-down | PASSED | browser/edge.log |
| B05 | Real Edge | mobile viewport without horizontal overflow and no uncaught page errors | PASSED | browser/edge.log |
| B06 | Real Edge | refresh gracefully recovered from a failed dashboard RPC | PASSED | browser/edge.log |
| R01 | P01 fresh+upgrade | 5 ORM cases each, 10 executions in baseline run | PASSED | baseline/p01-fresh.log; baseline/p01-upgrade.log |
| R02 | P01 standalone | 8 earlier cases rerun from the original source | PASSED | baseline/audit.log |
| R03 | P01 PostgreSQL | Archived independent import and retry | PASSED | baseline/p01-contention.log |
| R04 | P01 real Edge | Archived browser smoke | PASSED | baseline/browser.log |
| CON01 | Independent PostgreSQL | Identical overlap and replay | PASSED | security/contention.log |
| CON02 | Independent PostgreSQL | Conflicting batch rollback and safe retry | PASSED | security/contention.log |
| UP01 | Migration | Populated P01 clone, record hashes and XML IDs | PASSED | upgrade/retention.log |
| P01 | Performance | 50 instruments, 3750 candles, 50 snapshots | PASSED | performance/orm.json |
| BT01 | Synthetic correctness | CLI replay and reproducible experiment artifact | PASSED | backtesting/synthetic.json |
| SEC01 | Source inspection | Runtime Python/XML and forbidden endpoint signatures | PASSED | security/source-scan.log |
| D01 | Evidence | Archive and evidence checksum verification | PASSED | manifest.sha256 |
| EXT01 | SmartAPI | Authorized historical and quote smoke | BLOCKED | Account entitlements, credentials and egress |
| VAL01 | Quantitative research | Authorized market, holdout and financial validation | BLOCKED | No approved dataset or verified tariffs |
| PLAN01 | Planned test group | WebSocket and cross-process limits | NOT_RUN | See P02 specification §30 |
| PLAN02 | Planned test group | Corporate actions and reference ORM | NOT_RUN | See P02 specification §30 |
| PLAN03 | Planned test group | Actual cleared fee reconciliation | NOT_RUN | See P02 specification §30 |
| PLAN04 | Planned test group | Holdout and walk-forward | NOT_RUN | See P02 specification §30 |
| PLAN05 | Planned test group | Paper ledger and restart | NOT_RUN | See P02 specification §30 |
| PLAN06 | Planned test group | Dashboard themes/pagination/stale state | NOT_RUN | See P02 specification §30 |
| PLAN07 | Planned test group | Job and scheduler locking | NOT_RUN | See P02 specification §30 |
| PLAN08 | Planned test group | 100+ instrument benchmarks | NOT_RUN | See P02 specification §30 |

## 11 — Actual test execution evidence

| Command | Final evidence |
|---|---|
| `python -B -m unittest discover -s tests -p "unit_*.py" -v` | Exit 0, 18 passed. [Output](docs/evidence/p02/unit/python.log) |
| `./.local-test/p01-addons/golok_ai_trading_lab_pro/scripts/verify_odoo.ps1 -Browser -PostgresPort 55491 -HttpPort 18091 -Database golok_p02_p01_serial` | Archived source five ORM tests fresh and five upgrade, independent PostgreSQL test, and Edge PASSED. [Fresh](docs/evidence/p02/baseline/p01-fresh.log) · [Upgrade](docs/evidence/p02/baseline/p01-upgrade.log) · [Edge](docs/evidence/p02/baseline/browser.log) |
| `./scripts/verify_odoo.ps1 -Browser -Database golok_p02_final` | Exit 0, six fresh ORM and six upgrade ORM, two contention scenarios and six Edge checks. [Fresh](docs/evidence/p02/installation/fresh.log) · [Upgrade](docs/evidence/p02/installation/upgrade.log) · [Edge](docs/evidence/p02/browser/edge.log) |
| `./scripts/verify_p01_upgrade.ps1` | Exit 0, populated P01 upgrade then benchmark. [Migration](docs/evidence/p02/upgrade/retention.log) · [ORM performance](docs/evidence/p02/performance/orm.json) |
| `python -B scripts/run_backtest.py tests/fixtures/p02/spec.json tests/fixtures/p02/candles.csv` | Exit 0, one synthetic research trade, cost and stop policy verified. [Simulation artifact](docs/evidence/p02/backtesting/synthetic.json) |
| `python -B scripts/check_source.py` | Exit 0, 21 runtime files inspected. [Source check](docs/evidence/p02/security/source-scan.log) |

Expected unique-key warnings are produced by the duplicate tests. [P02 evidence manifest](docs/evidence/p02/manifest.sha256)

## 12 — Business invariant verification

| Requirement ID | Requirement | Status | Implementation | Test ID | Evidence | Remaining Work |
| --- | --- | --- | --- | --- | --- | --- |
| INV-01 | No real broker order execution | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-02 | No mandatory paid AI dependency | COMPLETE | `__manifest__.py`, `services/` | U01–U08 | `docs/evidence/tests/unit.log` | — |
| INV-03 | No GPU dependency | COMPLETE | `__manifest__.py`, `services/` | U01–U08 | `docs/evidence/tests/unit.log` | — |
| INV-04 | No fabricated live market data | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-05 | No actionable signal from stale required data | GUARD_ONLY | `services/research.py`, `models/lab.py` | O05–O06 | `docs/evidence/installation/{fresh,upgrade}.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-06 | No look-ahead bias | PARTIAL | `services/research.py`, `models/lab.py` | U07, O05 | `docs/evidence/tests/unit.log` | Close-time cutoff proven by snapshot assertion if ORM passes. Point-in-time vendor availability, survivorship and future execution tests remain. |
| INV-07 | No future information in historical decisions | PARTIAL | `services/research.py`, `models/lab.py` | U07, O05 | `docs/evidence/tests/unit.log` | Close-time cutoff proven by snapshot assertion if ORM passes. Point-in-time vendor availability, survivorship and future execution tests remain. |
| INV-08 | No duplicate market data records | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03–O04, O08 | `docs/evidence/installation/{fresh,upgrade}.log`, `docs/evidence/security/contention.log` | — |
| INV-09 | No duplicate paper-trade execution | NOT_STARTED | — | — | — | Required when virtual execution, costs and sizing are implemented. |
| INV-10 | No misleading profit guarantees | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-11 | No uncalibrated score represented as probability | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-12 | No unauthorized broker credential exposure | PARTIAL | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | No credential field or adapter exists. Add real sensitive-field and logging tests when integration is implemented. |
| INV-13 | No strategy promotion without validation | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-14 | No retrospective performance manipulation | PARTIAL | `services/research.py`, `models/lab.py` | O05, O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Snapshot input hashes and role-level immutability exist. Add experiment parameters, amendments and prospective outcomes. |
| INV-15 | No silent synthetic-data substitution | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-16 | No ignoring material transaction costs in net returns | NOT_STARTED | — | — | — | Required when virtual execution, costs and sizing are implemented. |
| INV-17 | No invalid position sizing | NOT_STARTED | — | — | — | Required when virtual execution, costs and sizing are implemented. |
| INV-18 | No cross-company unauthorized access | COMPLETE | `security/ir.access.csv`, `models/lab.py` | O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Add regression checks for future features and independent API calls. |
| INV-19 | No risk veto overridden by signal score | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-20 | No forced daily trading recommendation | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-21 | No experimental strategy presented as validated | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-22 | No real account capital allocation | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-23 | No unbounded background processing | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | U04, P01 | `docs/evidence/performance/services.csv` | Current paths are bounded and manual. Add bounded scheduling when implemented. |
| INV-24 | No paper profit represented as real profit | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-25 | No test marked PASSED without execution evidence | COMPLETE | `DEVELOPMENT_REPORT.md` | D01 | Sections 10–15 and 22 | No financial performance or production readiness claimed. |
| INV-26 | No unsupported market data entitlement bypass | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-27 | No missing required data treated as positive evidence | GUARD_ONLY | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Scope guard holds for existing paths. Future features need their own enforcement and tests. |
| INV-28 | No historical signal deletion to hide losses | PARTIAL | `services/research.py`, `models/lab.py` | O05, O07 | `docs/evidence/installation/{fresh,upgrade}.log` | Snapshot input hashes and role-level immutability exist. Add experiment parameters, amendments and prospective outcomes. |
| INV-29 | No dashboard KPI without a defined data source | COMPLETE | `__manifest__.py`, `models/lab.py` | S01 | `docs/evidence/security/source-scan.log` | Recheck when new paths are introduced. |
| INV-30 | No production-readiness claim with unresolved critical blockers | COMPLETE | `DEVELOPMENT_REPORT.md` | D01 | Sections 10–15 and 22 | No financial performance or production readiness claimed. |

## 13 — Acceptance criteria verification

| Requirement ID | Requirement | Status | Implementation | Test ID | Evidence | Remaining Work |
| --- | --- | --- | --- | --- | --- | --- |
| AC-001 | Odoo 20 Community compatibility verified | COMPLETE | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| AC-002 | Fresh installation successful | COMPLETE | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| AC-003 | Module upgrades safely | COMPLETE | `__manifest__.py`, `models/lab.py` | O01–O02 | `docs/evidence/installation/{fresh,upgrade}.log` | — |
| AC-004 | Zero mandatory paid AI APIs | COMPLETE | `__manifest__.py`, `services/` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Runtime manifest and expanded standard-library services verified. |
| AC-005 | CPU-only operation | COMPLETE | `__manifest__.py`, `services/` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | CPU-only synthetic ORM benchmark. |
| AC-006 | 16 GB hardware optimization measured | PARTIAL | `scripts/measure_services.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | 50 instruments measured in P02. Larger workloads pending. |
| AC-007 | Secure provider configuration | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Opt-in environment configuration tested offline; account authorization pending. |
| AC-008 | Instrument master synchronization | NOT_STARTED | `models/lab.py` | — | Manual registration only | Add verified provider instrument master sync and token mapping. |
| AC-009 | Historical market data ingestion | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Calendar-aware CSV implemented, broker history verified in fixtures. |
| AC-010 | Authorized live market data integration | BLOCKED | — | B01 | Decision and sources in §08 | Verify account terms, static egress and authorized credentials. Implement a read-only adapter. |
| AC-011 | Market data freshness enforcement | PARTIAL | `services/research.py`, `models/lab.py` | O05–O06 | `docs/evidence/installation/{fresh,upgrade}.log` | NO TRADE blocks actionable historical signals. Implement live freshness or expiry gates before enabling actionable signals. |
| AC-012 | Duplicate-data prevention | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03–O04, O08 | `docs/evidence/installation/{fresh,upgrade}.log`, `docs/evidence/security/contention.log` | — |
| AC-013 | Historical data provenance | COMPLETE | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | O03, O05 | `docs/evidence/installation/{fresh,upgrade}.log` | External verification of operator-supplied provenance remains. |
| AC-014 | Correct indicator calculations | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | 19 causal series implemented. Full independent reference verification pending. |
| AC-015 | Research engine interface operational | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Version 2 contract implemented for three results. |
| AC-016 | Applicable research capabilities functional | PARTIAL | `services/research.py`, `models/lab.py` | U06–U08, O05–O06 | `docs/evidence/tests/unit.log` | Three descriptive findings exist. Complete the remaining indicator set, evidence contract and engine methods. |
| AC-017 | Versioned strategy framework | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | ST-01 version and code hashes; general strategy lifecycle pending. |
| AC-018 | Market regime detection | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-019 | Explainable master decision engine | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | NO TRADE with temporal and quarantine gates. Master gates pending. |
| AC-020 | Transparent quality scoring | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-021 | Risk veto enforcement | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-022 | Transaction cost calculation | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Effective-dated cost engine works with documented hypothetical tariffs. |
| AC-023 | Expected net return calculation | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Synthetic net results v1. Validated evidence and calibration remain. |
| AC-024 | Position sizing validation | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Fee-aware sizing and stop risk verified for the synthetic slice. |
| AC-025 | Signal freshness and expiry | PARTIAL | `services/research.py`, `models/lab.py` | O05–O06 | `docs/evidence/installation/{fresh,upgrade}.log` | NO TRADE blocks actionable historical signals. Implement live freshness or expiry gates before enabling actionable signals. |
| AC-026 | Historical backtesting | PARTIAL | — | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Complete synthetic session replay. Authorized market and multi-session datasets pending. |
| AC-027 | Look-ahead bias prevention | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Cutoff, prefix invariance and next-opening rules tested; real data lineage pending. |
| AC-028 | Out-of-sample validation | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-029 | Walk-forward testing | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-030 | Reproducible research experiments | PARTIAL | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Synthetic code and data hashes verified. Holdout workflow pending. |
| AC-031 | Automatic paper trading | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-032 | Virtual cash integrity | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-033 | Paper execution idempotency | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-034 | Paper portfolio reporting | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-035 | Strategy performance tracking | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-036 | Recommendation monitoring | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-037 | Automatic research scheduling | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-038 | Scheduler concurrency protection | NOT_STARTED | — | — | — | See criterion-specific verification in report §13. |
| AC-039 | Premium dashboard operational | PARTIAL | `static/src/`, `views/lab.xml`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Native historical plot and company KPI additions. Full dashboards A–I incomplete. |
| AC-040 | Dashboard KPI correctness | COMPLETE | `static/src/`, `views/lab.xml`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Current overview KPI/fixture chart values verified in Edge. |
| AC-041 | Real browser UI verified | PARTIAL | `scripts/verify_browser.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Six focused real-browser checks. Full chart/filters/themes coverage incomplete. |
| AC-042 | Security permissions verified | COMPLETE | `security/ir.access.csv`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Current ACLs reverified, including calendar administration and forged research creation. |
| AC-043 | Company isolation verified | COMPLETE | `security/ir.access.csv`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Company isolation regression passed. |
| AC-044 | Credential redaction verified | PARTIAL | `__manifest__.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Credential redaction checked with offline failure fixtures. No actual credential run. |
| AC-045 | Recovery behavior verified | PARTIAL | `services/market_data.py`, `wizard/lab.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Independent conflicting imports and retry verified. |
| AC-046 | No real-order functionality | COMPLETE | `__manifest__.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Mandatory prohibition verified by runtime endpoint rejection and source scan. |
| AC-047 | NO TRADE behavior verified | COMPLETE | `services/research.py`, `models/lab.py` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | NO TRADE verified in ORM and browser. |
| AC-048 | No fabricated performance results | COMPLETE | `DEVELOPMENT_REPORT.md` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | Only synthetic correctness evidence reported. |
| AC-049 | Complete setup and user documentation | PARTIAL | `README.md` | D01 | README and §21 | Document setup for functionalities as they are implemented. |
| AC-050 | Evidence-backed development report generated | COMPLETE | `DEVELOPMENT_REPORT.md` | See P02 test inventory | `docs/evidence/p02/manifest.sha256` | P02 handoff and manifest verified. |

| Criterion | Requirement | Status | Outcome | Evidence or source |
| --- | --- | --- | --- | --- |
| P02-AC-001 | P01 baseline preserved | PASSED | Migration and populated retention | verify_p01_upgrade.ps1; upgrade/retention.log |
| P02-AC-002 | Previous defects independently revalidated | PASSED | P01 reruns and P02 browser/ORM regression | baseline/audit.log; baseline/browser.log |
| P02-AC-003 | Traceability semantics corrected | PASSED | Semantic guards, prohibitions and optional technologies separated | REQUIREMENTS_TRACEABILITY.md |
| P02-AC-004 | Evidence integrity verified | PASSED | P01 and P02 manifest verification | baseline/audit.log; manifest.sha256 |
| P02-AC-005 | Source checkpoint established | PASSED | Verified recovery archive | history/P01-source.zip; baseline/source.sha256 |
| P02-AC-006 | Exchange calendar service implemented | PASSED | Explicit versioned NSE and BSE calendar records | services/calendar.py; unit/python.log |
| P02-AC-007 | Session-aware candle validation | PASSED | Grid mismatch, closed days, cutoffs and missing observations | installation/fresh.log; unit/python.log |
| P02-AC-008 | Point-in-time data contract | PASSED | Opening, closing, publication, ingestion and cutoff semantics | models/lab.py; installation/fresh.log |
| P02-AC-009 | Instrument reference mapping integrity | PARTIAL | Independent reference resolver; ORM persistence and provider wiring pending | services/reference.py; unit/python.log |
| P02-AC-010 | Data quality eligibility enforcement | PARTIAL | Temporal and quarantine guards; source verification and unified eligibility incomplete | models/lab.py; installation/fresh.log |
| P02-AC-011 | Synthetic-data isolation | PASSED | Fixtures have explicit origin and calendar constraints | models/lab.py; unit/python.log |
| P02-AC-012 | Read-only provider interface | PASSED | Fixed REST allowlist and disabled default transport | services/smartapi.py; unit/python.log |
| P02-AC-013 | SmartAPI adapter fixture tests | PASSED | Deterministic fixture login, history and quote | tests/unit_p02.py; unit/python.log |
| P02-AC-014 | Provider timeout and rate-limit protection | PASSED | Client-local timeout, pacing and response limits | services/smartapi.py; unit/python.log |
| P02-AC-015 | Secure credential handling | PASSED | Environment and process-local tokens with sanitized fixture failures | services/smartapi.py; unit/python.log |
| P02-AC-016 | Live verification correctly classified | PASSED | No authenticated live request made | SMARTAPI_SETUP.md |
| P02-AC-017 | Technical indicator mathematical verification | PARTIAL | All 19 indicators implemented; full independent numerical cross-verification is incomplete | INDICATOR_FORMULAS.md; unit/python.log |
| P02-AC-018 | Indicator prefix invariance | PASSED | All 19 series checked at five prefixes of a reference fixture | tests/unit_p02.py; unit/python.log |
| P02-AC-019 | Versioned research engine contract | PARTIAL | Version 2 contract covers three ORM engines. Other engines remain pending. | models/lab.py; installation/fresh.log |
| P02-AC-020 | Effective-dated transaction costs | PASSED | Decimal, per-side and effective-dated tariffs with hypothetical inputs | services/simulation.py; unit/python.log |
| P02-AC-021 | Fee-aware position sizing | PASSED | Fee-adjusted capital, risk and liquidity constraints | services/simulation.py; unit/python.log |
| P02-AC-022 | Independent risk veto | PASSED | Independent net reward-to-risk veto | services/simulation.py; unit/python.log |
| P02-AC-023 | Versioned strategy framework | PARTIAL | Code-hashed ST-01 specification. Persistent framework and approval workflow pending. | services/backtest.py; backtesting/synthetic.json |
| P02-AC-024 | ST-01 research strategy implementation | PARTIAL | Research-only synthetic single-session candidate. Full historical strategy cycle pending. | services/backtest.py; backtesting/synthetic.json |
| P02-AC-025 | Conservative historical simulation | PASSED | Later openings, stop-first ambiguity and conservative exits in one-session replay | services/backtest.py; unit/python.log |
| P02-AC-026 | Backtest reproducibility | PASSED | Frozen parameters, code and dataset digests; deterministic replay | services/backtest.py; backtesting/synthetic.json |
| P02-AC-027 | Holdout isolation | PARTIAL | Partition label exists; temporal split and one-time holdout enforcement are missing | docs/BACKTEST_EXECUTION_POLICY.md |
| P02-AC-028 | Financial performance provenance | PASSED | Synthetic provenance is explicit; no validated-market sample or reported market performance | backtesting/synthetic.json |
| P02-AC-029 | Structured NO TRADE enforcement | PARTIAL | Existing NO TRADE and individual reasons; fourteen-gate pipeline incomplete | models/lab.py; installation/fresh.log |
| P02-AC-030 | No actionable real-market recommendation leakage | PASSED | Historical/fixture-only decisions, no executable path | unit/python.log; security/source-scan.log |
| P02-AC-031 | Virtual ledger integrity | NOT_RUN | Virtual ledger deferred pending broader validation | docs/DEVELOPMENT_PLAN.md |
| P02-AC-032 | Virtual execution idempotency | NOT_RUN | Virtual fill idempotency deferred with ledger | docs/DEVELOPMENT_PLAN.md |
| P02-AC-033 | Premium OWL dashboard improvements | PARTIAL | Overview, chart, quarantine and data provenance; remaining terminal areas incomplete | static/src; browser/edge.log |
| P02-AC-034 | Actual database-backed chart values | PASSED | Actual bounded chart values tested through the browser and ORM | browser/edge.log; installation/fresh.log |
| P02-AC-035 | Authorized dashboard drill-downs | PASSED | Company and permission checked chart and existing native drill-down | browser/edge.log; installation/fresh.log |
| P02-AC-036 | Real browser verification | PARTIAL | Six real Edge checks passed; requested full theme, pagination and stale coverage remains | browser/edge.log |
| P02-AC-037 | End-to-end performance measurement | PASSED | Measured 50 instruments through ORM import and research | performance/orm.json |
| P02-AC-038 | Resource-bound execution | PARTIAL | Core paths bounded; job constraints and configured deadlines pending | services; performance/orm.json |
| P02-AC-039 | Complete security regression | PARTIAL | Targeted ACL, company, forged create, quarantine and endpoint checks; complete program pending | installation/fresh.log; unit/python.log |
| P02-AC-040 | Updated evidence-backed development report | PASSED | Updated 22-section handoff, matrices and validated checksums | DEVELOPMENT_REPORT.md; manifest.sha256 |

## 14 — Financial research results

The synthetic fixture has nine five-minute bars, one session, one simulated stop-first trade, and hypothetical transaction charges. Experiment fingerprint `e3ed346ea5b7fc5975590bd17f23bb8975281df0e12cbac4c4c5c583a4d2dbca`. The saved artifact contains the strategy/code, dataset and cost parameters. Dollar or INR outcomes in it belong solely to the correctness fixture. No authorized historical, out-of-sample, walk-forward or prospective paper trial was run. Win rate, profitability, statistical uncertainty and real-market results remain unavailable.

## 15 — Performance results

50 instruments × 75 candles, 3,750 rows; 361 SQL statements. Wall time 5.247 s, ingestion 2.451 s, research 1.354 s, active-company count query 3.97 ms. Odoo shell process used 3.531 CPU s and sampled peak RSS 138.4 MiB. System available RAM at start was 4.11 GiB.

The benchmark exercised actual ORM parsing, import, research and persistence on synthetic data. SQL count and process metrics were measured through Python on the target workstation. PostgreSQL resident memory and UI response latency were not separately profiled. No 100-, 250-, 500-, or 1,000-instrument end-to-end claim is made. [Results](docs/evidence/p02/performance/orm.json)

## 16 — Security verification

Baseline rules and company isolation reran. A prior research creation could reach the idempotent return before checking create permission. P02 now checks permission first, restricts valid RPC dataset identifiers and gives a uniform denied result for absent or inaccessible datasets. The calendar-role test checks unauthorized create and immutable history; quarantine is restricted to System Administrators. The native chart is active-company scoped and checks the source digest. Two genuine PostgreSQL race tests verify identical replay and atomic rollback on a conflicting import. Endpoint restrictions were tested using the fixture transport and an unsupported operation. The full risk-manager and configuration penetration program remains incomplete.

## 17 — Errors and bug fixes

| ID | Result |
|---|---|
| AUD-001 | P01 security, Odoo BinaryValue, Sass, OWL 3 and setup fixes were independently exercised by archived ORM/Edge tests. The initial parallel Edge pass hit a session disconnect. The serial rerun passed. |
| AUD-002 | P01 requirement descriptions for prohibited real orders were corrected. Original IDs and original evidence files were retained. |
| AUD-003 | Moved research create authorization before the idempotent return; confirmed with a forged Viewer call in the ORM suite. |
| ENV-02 | Wrapping the entire PowerShell harness in a pipeline stalled PostgreSQL subprocess handling. Direct execution resolved it. The parallel test pass also showed a shared default HTTP test-port collision. The P02 script now explicitly assigns a dedicated test port. |

## 18 — Incomplete features

Exchange revisions remain operator-curated. Calendar compatibility for closing auctions, split sessions and reference history still needs broader exchange data. Persist effective-dated reference and corporate-action provenance, then implement a verified provider-to-ORM ingestion contract, monitoring and an authorization review. Complete the remaining research engines, strategy and gate lifecycles, verified tariffs, multi-session and holdout rules, paper ledger, job recovery and the remaining dashboard panels. The linked matrix includes every original and P02 requirement and the named missing test groups appear in section 10.

## 19 — Development completion metrics

Archived P01 reported 72/1,236. Reapplying the old counting convention to original IDs for comparison gives 73/1,236, counting verified prohibitions and features already locked out as the old rubric did. The corrected capability-and-process measure is 56/1210; it removes each row marked OPTIONAL, GUARD_ONLY, CONSTRAINT_VERIFIED or DEFERRED_OUT_OF_SCOPE. It is a requirements measure, not a product estimate. Among 23 tracked P02 functional milestones drawn from the P02 acceptance list, 11 passed. P02 acceptance passed 26/40, with 14/50 original ACs either revalidated or still relevant at the documented scope. There are 796 detailed P02 requirement IDs preserved as tracking lines and excluded from these milestone ratios. Research engine results exist for 3/25, all partial against full definitions. One of 20 strategies is implemented in synthetic scope, and 0 are financially validated.

Constraint compliance is scoped to audited paths. External live integration remains blocked and financially validated strategies remain zero. Neither is included in executable capability progress.

## 20 — Next development recommendations

1. Persist company-scoped versioned reference data from `services/reference.py` and connect verified price adjustments and vendor publication lineage to `models/lab.py`.
2. Confirm Angel One entitlements and egress. Extend `services/smartapi.py` with authorized integration diagnostics and an authenticated smoke test that uses no order routes.
3. Add immutable experiment partitions, multi-session events and recorded tariff evidence around `services/backtest.py` and `services/simulation.py`. Expand synthetic adverse scenarios before any market experiment.
4. After those gates, implement virtual accounting and locking with restart tests, then expose reconciled simulator data in OWL.

## 21 — Owner setup instructions

Install or upgrade the module through normal local Odoo administration. Back up and test an upgrade on a clone first. Assign the Trading Lab roles, then create an instrument and optional calendar revision. Use the corresponding legacy or temporal CSV format. Run research and open the overview chart. Reproduce the sample strategy with the CLI in the setup guide. SmartAPI is offline within Odoo and requires separate authorization before any external smoke test. [Setup guide](README.md)

## 22 — Final readiness decision

**FOUNDATION VERIFIED** for company-scoped calendar-bound descriptive research and conservative synthetic replay. The business scope excludes real orders and real account balances. Authorized market data, effective verified tariffs, immutable holdout isolation and financial evidence are needed before historical strategy validation. The next milestone should complete those prerequisites and retain the same fail-closed restriction.
