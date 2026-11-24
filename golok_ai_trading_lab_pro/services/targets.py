"""Causal target levels and an explicitly labeled simulation benchmark."""

from decimal import Decimal

VERSION = "structure-1"


def levels(history, entry, stop, release, after_open, exit_cutoff):
    if not stop < entry or after_open >= exit_cutoff:
        return (), "INVALID_STOP_OR_SESSION"
    if release == "fixed_4r":
        return (entry + (entry - stop) * 4,), "EXPLICIT_FIXED_4R_BENCHMARK"
    if release != "structure":
        raise ValueError("Unknown target policy.")
    # Nearest completed resistance is the first barrier. A farther level cannot
    # rescue a poor risk/reward ratio at the nearest one.
    highs = {bar.high for bar in history[-20:] if bar.available_at < after_open and bar.high > entry}
    return ((min(highs),), "NEAREST_COMPLETED_RESISTANCE") if highs else ((), "NO_CAUSAL_TARGET")


def rank(sizing, volume):
    ratio = sizing.reward / sizing.loss if sizing.loss and sizing.reward is not None else Decimal("-1")
    return ratio >= 3, ratio, sizing.reward or Decimal(0), volume
