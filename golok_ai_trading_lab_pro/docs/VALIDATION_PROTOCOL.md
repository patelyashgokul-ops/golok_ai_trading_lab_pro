# Synthetic and financial validation

Current Odoo experiments freeze input digest, calendar revision, strategy, tariff revision, risk and code identity. They cover a single synthetic instrument across up to 31 calendar days and 4,000 observations. Missing sessions stop replay rather than creating prices. Unsupported sessions and unresolved exits retain any preceding results and cannot be posted to the virtual ledger.

P05 portfolio replay freezes each series digest, exchange calendar, hypothetical tariff, strategy release and code identity. It supports up to 16 distinct synthetic instruments and 12,000 bars across at most 31 calendar dates. The virtual ledger records every fill and closure. The current closed-day drawdown measures daily ending cash.

The standalone temporal module freezes independent date tuples for training, validation and final holdout, requires an explicit period embargo and produces rolling folds from training and prior validation dates. The holdout is excluded from fold construction. In Odoo, seal an unused synthetic date window after training. The app protects the instrument and date window across source aliases, jobs and comparison records. A Risk Manager in the active company can run the frozen evaluation once. Actual historical panels, licensed point-in-time lineage, fully verified tariffs and genuine prospective paper evidence remain pending.
