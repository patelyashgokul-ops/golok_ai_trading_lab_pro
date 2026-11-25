"""Causal target levels and an explicitly labeled simulation benchmark."""

from decimal import Decimal

from . import indicators

VERSION = "structure-1"
EXPERIMENTAL_VERSION = "atr-barrier-1"
JOINT_POLICY = "causal_levels"
POLICY_CHOICES = (("structure", "Completed market structure"), ("fixed_4r", "Fixed 4R benchmark"),
                  ("atr_barrier", "Experimental ATR-capped resistance"),
                  (JOINT_POLICY, "Experimental causal entry, stop and target"))
POLICIES = tuple(code for code, _label in POLICY_CHOICES)


def levels(history, entry, stop, release, after_open, exit_cutoff):
    if not stop < entry or after_open >= exit_cutoff:
        return (), "INVALID_STOP_OR_SESSION"
    if release == "fixed_4r":
        return (entry + (entry - stop) * 4,), "EXPLICIT_FIXED_4R_BENCHMARK"
    if release not in ("structure", "atr_barrier"):
        raise ValueError("Unknown target policy.")
    # Nearest completed resistance is the first barrier. A farther level cannot
    # rescue a poor risk/reward ratio at the nearest one.
    highs = {bar.high for bar in history[-20:] if bar.available_at < after_open and bar.high > entry}
    if not highs:
        return (), "NO_CAUSAL_TARGET"
    if release == "structure":
        return (min(highs),), "NEAREST_COMPLETED_RESISTANCE"
    completed = [bar for bar in history[-20:] if bar.close_time <= bar.available_at < after_open]
    if len(completed) < 15:
        return (), "INSUFFICIENT_VOLATILITY_HISTORY"
    atr = indicators.calculate(completed)["atr14"][-1]
    if not atr:
        return (), "INSUFFICIENT_VOLATILITY_HISTORY"
    return (min(min(highs), entry + 2 * atr),), "NEAREST_RESISTANCE_WITH_ATR_CAP"


def rank(sizing, volume):
    return rank_values(sizing.reward, sizing.loss, volume)


def rank_values(reward, loss, volume):
    ratio = reward / loss if loss and reward is not None else Decimal("-1")
    return ratio >= 3, ratio, reward or Decimal(0), volume


def competition_evidence():
    return {
        "rank_version": "cost-aware-1",
        "financial_validation": "UNAVAILABLE",
        "net_expectancy": None,
        "out_of_sample_trades": None,
        "out_of_sample_drawdown": None,
        "parameter_stability": None,
        "cost_sensitivity": None,
        "market_regime_compatibility": None,
    }
