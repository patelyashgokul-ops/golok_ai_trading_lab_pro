"""Repeatable, visibly artificial session data for offline verification."""

from decimal import Decimal
from random import Random

from .market_data import Candle

VERSION = "fixture-1"
SEED = 8105


def generate(sessions, seconds=300):
    if not 1 <= len(sessions) <= 31 or any(session.segments for session in sessions.values()):
        raise ValueError("Use up to 31 explicit fixture dates without split sessions.")
    random = Random(SEED)
    bars = []
    for day, session in sorted(sessions.items()):
        price = Decimal(100)
        for opening, close in session.slots(seconds):
            change = Decimal(random.randrange(-6, 7)) / 20
            end = price + change
            bars.append(Candle(close, price, max(price, end) + Decimal(".10"), min(price, end) - Decimal(".10"),
                               end, random.randrange(800, 2001), opening, close))
            price = end
    if not bars or len(bars) > 4000:
        raise ValueError("Use a fixture calendar containing 1–4,000 five-minute observations.")
    return bars
