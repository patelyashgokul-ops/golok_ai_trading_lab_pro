"""Plan disjoint training, validation and evaluation windows over trading dates."""

VERSION = "p09-walk-forward-1"
GRID_VERSION = "r01-policy-grid-1"


def folds(days, *, training, validation, evaluation, embargo, expanding):
    if (days != sorted(set(days)) or len(days) > 31
            or any(type(value) is not int or not 1 <= value <= 10 for value in (training, validation, evaluation, embargo))):
        raise ValueError("Use distinct chronological dates and 1–10 trading sessions for each window.")
    width = training + validation + evaluation + 2 * embargo
    for offset in range(0, len(days) - width + 1, evaluation):
        train_end = offset + training
        valid_start = train_end + embargo
        valid_end = valid_start + validation
        test_start = valid_end + embargo
        yield {
            "training": days[0 if expanding else offset:train_end],
            "validation": days[valid_start:valid_end],
            "evaluation": days[test_start:test_start + evaluation],
        }


def rank_summary(metrics):
    if metrics["trade_count"] < 2 or metrics["expectancy"] <= 0:
        return None
    drawdown = metrics["closed_trade_cash_drawdown"]["amount"]
    return metrics["expectancy"], -drawdown, metrics["trade_count"], -metrics["fees"]


def choose_training_trial(trials):
    """Use only already-produced training trials, with explicit deterministic ties."""
    scored = [(rank_summary(trial["metrics"]), trial) for trial in trials]
    eligible = sorted((row for row in scored if row[0] is not None),
                      key=lambda row: (row[1]["strategy"], row[1]["target_policy"]))
    return max(eligible, key=lambda row: row[0])[1] if eligible else None
