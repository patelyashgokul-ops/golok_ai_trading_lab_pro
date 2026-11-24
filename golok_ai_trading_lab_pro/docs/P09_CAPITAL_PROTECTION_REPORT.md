# P09 virtual capital protection

Fixture accounts open at ₹50,000. Each order applies the existing 0.5% planned-loss limit, 2:1 minimum modeled net reward-to-risk and 1% participation cap. The account enforces one live virtual exposure, three new entries per day, a 1% daily loss threshold and suspension after two consecutive losses. The pause action releases pending cash and risk, records the operator and preserves open exposure. Reconciliation can continue while paused. Explicit resume requires a risk manager and no unresolved exposure.

The journal uses integer paise. After each transition, available cash plus reserved cash plus open position cost must equal opening virtual cash plus realized net P&L. Maximum modeled risk does not cap realized loss during a gap. Sector, portfolio-wide concentration, correlation and marked unrealized downside remain open.
