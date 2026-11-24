"""Exact paise reconciliation for completed historical research trades."""

from decimal import Decimal, InvalidOperation

MAX_CASH = 2_147_483_647


def paise(value):
    try:
        amount = Decimal(value)
        if not amount.is_finite() or abs(amount) > Decimal(MAX_CASH) / 100:
            raise ValueError
        scaled = amount * 100
        if scaled != scaled.to_integral_value():
            raise ValueError
        return int(scaled)
    except (TypeError, ValueError, InvalidOperation):
        raise ValueError("Virtual cash must be representable in whole paise.") from None


def postings(trades, available):
    """Return events whose virtual cash and position reconcile after each trade."""
    lines = []
    for sequence, trade in enumerate(trades, 1):
        quantity = trade["quantity"]
        if type(quantity) is not int or not 0 < quantity <= MAX_CASH:
            raise ValueError("Invalid synthetic trade quantity.")
        buy = paise(Decimal(trade["entry"]) * quantity)
        sell = paise(Decimal(trade["exit"]) * quantity)
        buy_fee = sum(paise(value) for value in trade["buy_fees"].values())
        sell_fee = sum(paise(value) for value in trade["sell_fees"].values())
        reserve = buy + buy_fee
        proceeds = sell - sell_fee
        if min(buy, sell) <= 0 or min(buy_fee, sell_fee, proceeds) < 0 or reserve > available:
            raise ValueError("Insufficient virtual cash or unsupported simulated fees.")
        realized = proceeds - reserve
        if realized != paise(trade["net"]):
            raise ValueError("The experiment does not reconcile to whole paise.")
        available -= reserve
        lines.append(dict(sequence=sequence, kind="reserve", cash_delta=-reserve, reserved_delta=reserve,
                          quantity_delta=0, fee=0, realized=0, available_after=available, reserved_after=reserve))
        lines.append(dict(sequence=sequence, kind="buy_fill", cash_delta=0, reserved_delta=-reserve,
                          quantity_delta=quantity, fee=buy_fee, realized=0, available_after=available, reserved_after=0))
        available += proceeds
        if available > MAX_CASH:
            raise ValueError("Virtual cash exceeds the supported account limit.")
        lines.append(dict(sequence=sequence, kind="sell_fill", cash_delta=proceeds, reserved_delta=0,
                          quantity_delta=-quantity, fee=sell_fee, realized=realized, available_after=available, reserved_after=0))
    return available, lines
