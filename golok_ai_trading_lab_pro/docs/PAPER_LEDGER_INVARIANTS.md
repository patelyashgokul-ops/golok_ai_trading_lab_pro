# Virtual historical replay ledger

Only completed, non-quarantined synthetic experiments with trades can be posted. Risk Managers choose an active-company virtual account. A database row lock and unique batch key serialize posts and make repeated posting return the previous batch. Earlier or overlapping new experiment windows fail closed.

Money uses whole paise. A reservation moves entry notional and entry fees out of available cash into reserved cash. The virtual entry consumes that exact reservation and opens a quantity. A virtual close reduces that quantity to zero and credits proceeds after the recorded exit fee. Realized P&L is credited proceeds minus entry notional and entry fee. Ledger reconstruction checks that quantities and reserves close at zero and cash equals opening plus all cash deltas. A reconciliation failure rolls back the batch, events and balance together.

This feature posts closed historical replay events; it has no persistent overnight positions, partial fills, feed-driven stops, prospective cash, deposits beyond genesis, live execution, Odoo accounting moves or broker access.
