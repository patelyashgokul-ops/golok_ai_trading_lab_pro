"""Decimal transaction costs and independent historical sizing."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_EVEN, ROUND_HALF_UP

ZERO = Decimal(0)
PAISE = Decimal("0.01")
ROUNDING = {"half_up": ROUND_HALF_UP, "half_even": ROUND_HALF_EVEN, "down": ROUND_DOWN}
STATUTORY = {"stt", "exchange", "sebi", "gst", "stamp", "other"}
FRICTION = {"spread", "slippage"}
CHARGES = {"brokerage", *STATUTORY, *FRICTION}


def finite(value):
    return isinstance(value, Decimal) and value.is_finite()


@dataclass(frozen=True)
class Tariff:
    name: str
    starts: date
    ends: date | None
    exchange: str
    segment: str
    side: str
    basis: str
    amount: Decimal
    source: str
    verification: str = "hypothetical"
    minimum: Decimal = ZERO
    maximum: Decimal | None = None
    rounding: str = "half_up"

    def __post_init__(self):
        if (self.name not in CHARGES or self.exchange not in ("NSE", "BSE") or self.segment != "equity_intraday"
                or self.side not in ("buy", "sell") or self.basis not in ("turnover", "fixed", "tax_base")
                or self.rounding not in ROUNDING or not isinstance(self.source, str) or not self.source.strip()
                or self.verification not in ("hypothetical", "documented")
                or type(self.starts) is not date or (self.ends is not None and (type(self.ends) is not date or self.ends <= self.starts))
                or not finite(self.amount) or self.amount < 0 or not finite(self.minimum) or self.minimum < 0
                or (self.maximum is not None and (not finite(self.maximum) or self.maximum < self.minimum))
                or (self.basis == "tax_base") != (self.name == "gst")):
            raise ValueError("Invalid tariff or provenance.")

    def applies(self, day, exchange, side):
        return self.exchange == exchange and self.side == side and self.starts <= day and (self.ends is None or day < self.ends)

    def calculate(self, turnover, tax_base):
        raw = {"turnover": turnover * self.amount, "fixed": self.amount, "tax_base": tax_base * self.amount}[self.basis]
        bounded = max(raw, self.minimum)
        if self.maximum is not None:
            bounded = min(bounded, self.maximum)
        return bounded.quantize(PAISE, rounding=ROUNDING[self.rounding])


class CostSchedule:
    def __init__(self, tariffs):
        self.tariffs = tuple(tariffs)
        if not 1 <= len(self.tariffs) <= 100:
            raise ValueError("Supply 1–100 explicit tariffs.")

    def fees(self, day, exchange, side, price, quantity, *, embedded_friction=False):
        if type(quantity) is not int or quantity <= 0 or not finite(price) or price <= 0:
            raise ValueError("Cost calculation requires a positive price and whole-share quantity.")
        active = [rule for rule in self.tariffs if rule.applies(day, exchange, side)]
        names = {rule.name for rule in active}
        required = {"brokerage", "stt", "exchange", "sebi", "gst", "stamp"}
        if not embedded_friction:
            required |= FRICTION
        if not required <= names or len(names) != len(active):
            raise ValueError("Required tariffs are missing or overlapping.")
        turnover = price * quantity
        fees = {rule.name: rule.calculate(turnover, ZERO) for rule in active if rule.name != "gst"
                and not (embedded_friction and rule.name in FRICTION)}
        # The supported GST base is documented for this simulation contract.
        tax_base = sum((fees.get(name, ZERO) for name in ("brokerage", "exchange", "sebi")), ZERO)
        gst = next(rule for rule in active if rule.name == "gst")
        fees["gst"] = gst.calculate(turnover, tax_base)
        return fees


@dataclass(frozen=True)
class RiskPolicy:
    capital: Decimal = Decimal("50000")
    risk_fraction: Decimal = Decimal("0.005")
    minimum_rr: Decimal = Decimal("2")
    liquidity_fraction: Decimal = Decimal("0.01")
    adverse_ticks: int = 1


@dataclass(frozen=True)
class Sizing:
    quantity: int
    reason: str
    loss: Decimal | None = None
    reward: Decimal | None = None


def size_long(entry, stop, target, tick, volume, day, exchange, schedule, policy=RiskPolicy()):
    values = (entry, stop, target, tick, policy.capital, policy.risk_fraction, policy.minimum_rr, policy.liquidity_fraction)
    if (not all(finite(value) for value in values) or tick <= 0 or not 0 < stop < entry < target
            or any(price % tick for price in (entry, stop, target))
            or policy.capital <= 0 or not 0 < policy.risk_fraction <= 1 or policy.minimum_rr <= 0
            or not 0 < policy.liquidity_fraction <= 1 or type(policy.adverse_ticks) is not int or policy.adverse_ticks < 0):
        return Sizing(0, "INVALID_RISK_INPUT")
    if type(volume) is not int or volume <= 0:
        return Sizing(0, "INSUFFICIENT_LIQUIDITY")
    stressed = stop - tick * policy.adverse_ticks
    if stressed <= 0:
        return Sizing(0, "INVALID_STRESSED_STOP")

    def fees(side, price, quantity):
        return sum(schedule.fees(day, exchange, side, price, quantity).values())

    def limits(quantity):
        buy_fee = fees("buy", entry, quantity)
        loss = (entry - stressed) * quantity + buy_fee + fees("sell", stressed, quantity)
        cash = entry * quantity + buy_fee
        return buy_fee, loss, cash

    maximum = min(int(policy.capital // entry), int(volume * policy.liquidity_fraction))
    if maximum <= 0:
        return Sizing(0, "INSUFFICIENT_CAPITAL_OR_LIQUIDITY")
    low, high = 0, maximum
    try:
        while low < high:
            quantity = (low + high + 1) // 2
            _, loss, cash = limits(quantity)
            if cash <= policy.capital and loss <= policy.capital * policy.risk_fraction:
                low = quantity
            else:
                high = quantity - 1
        if low == 0:
            return Sizing(0, "INSUFFICIENT_CAPITAL_OR_RISK_BUDGET")
        buy_fee, loss, _ = limits(low)
        reward = (target - entry) * low - buy_fee - fees("sell", target, low)
    except ValueError:
        return Sizing(0, "COST_MODEL_UNAVAILABLE")
    if reward < policy.minimum_rr * loss:
        return Sizing(0, "MINIMUM_NET_REWARD_TO_RISK", loss, reward)
    return Sizing(low, "SIMULATION_ONLY", loss, reward)
