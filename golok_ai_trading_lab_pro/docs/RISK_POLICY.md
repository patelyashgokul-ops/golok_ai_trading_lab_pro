# Synthetic execution and risk limits

ST-01 multi-2 stops after the second consecutive net loss for the remainder of that experiment. A nonloss trade resets the streak before suspension; a closed session or a session without a trade leaves it unchanged. There is no automatic override or resume within an experiment. Historical replay posting must match frozen starting capital to the account’s available cash under the account lock.

P03 uses the existing fee-aware risk gate with 0.5% planned exposure, net reward-to-risk of at least 2, whole shares, a one-tick adverse stop allowance and prior-candle liquidity limits. Only virtual capital is used. ST-01 replays one long trade per regular session. The Odoo experiment sets reference capital and compounds realized daily virtual cash across sessions. Real downside can exceed planned exposure. Aggregate cross-instrument limits, a daily loss circuit breaker and prospective portfolio sizing are pending.
