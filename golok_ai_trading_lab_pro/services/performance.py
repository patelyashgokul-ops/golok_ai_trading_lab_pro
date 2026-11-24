"""Reconcile completed virtual trades and report explicitly sampled drawdowns."""

from decimal import Decimal


VERSION = "p09-performance-1"
ZERO = Decimal(0)


def amount(value):
    if isinstance(value, (bool, float)):
        raise ValueError("Use exact decimal values for financial metrics.")
    number = Decimal(value)
    if not number.is_finite():
        raise ValueError("Non-finite financial input.")
    return number


def drawdown(opening, observations):
    if not observations:
        return None
    peak = opening
    peak_time = None
    duration = 0
    result = {"amount": ZERO, "fraction": ZERO, "peak": None, "trough": None, "duration_samples": 0}
    for timestamp, equity in observations:
        if equity >= peak:
            peak, peak_time = equity, timestamp
            duration = 0
        else:
            duration += 1
        if peak - equity > result["amount"]:
            result = {"amount": peak - equity, "fraction": (peak - equity) / peak,
                      "peak": peak_time, "trough": timestamp, "duration_samples": duration}
    return result


def summarize(result):
    opening = amount(result["initial_cash"])
    ending = amount(result["ending_cash"])
    if opening <= 0 or ending < 0:
        raise ValueError("Invalid portfolio balances.")
    gross_wins, gross_losses, fees, net, turnover = (ZERO,) * 5
    wins, losses, multiples = [], [], []
    win_streak = loss_streak = best_win = best_loss = 0
    closed_cash = opening
    closed_samples = []
    for trade in result["trades"]:
        gross, costs, outcome = (amount(trade[key]) for key in ("gross", "fees", "net"))
        quantity = trade["quantity"]
        if costs < 0 or gross - costs != outcome or type(quantity) is not int or quantity <= 0:
            raise ValueError("A trade does not reconcile.")
        gross_wins += max(gross, ZERO)
        gross_losses += min(gross, ZERO)
        fees += costs
        net += outcome
        turnover += (amount(trade["entry"]) + amount(trade["exit"])) * quantity
        if outcome > 0:
            wins.append(outcome)
        elif outcome < 0:
            losses.append(outcome)
        win_streak = win_streak + 1 if outcome > 0 else 0
        loss_streak = loss_streak + 1 if outcome < 0 else 0
        best_win, best_loss = max(best_win, win_streak), max(best_loss, loss_streak)
        risk = amount(trade["loss"])
        if risk > 0:
            multiples.append(outcome / risk)
        closed_cash += outcome
        closed_samples.append((trade["exit_time"], closed_cash))
    count = len(result["trades"])
    if (net != ending - opening or net != amount(result["net"]) or fees != amount(result["fees"])
            or gross_wins + gross_losses != amount(result["gross"])):
        raise ValueError("Reported balances, trades and fees do not reconcile.")
    eod = [(point["date"], amount(point["cash"])) for point in result["days"]]
    if eod and eod[-1][1] != ending:
        raise ValueError("End-of-day cash does not match ending cash.")
    return {
        "version": VERSION, "scope": "SYNTHETIC_SOFTWARE_ONLY",
        "status": "SOFTWARE_VERIFIED" if count else "INSUFFICIENT_TRADES",
        "initial_cash": opening, "ending_cash": ending, "ending_equity": ending,
        "gross_wins": gross_wins, "gross_losses": gross_losses, "gross": gross_wins + gross_losses,
        "fees": fees, "net": net, "net_return": net / opening, "turnover": turnover,
        "trade_count": count, "wins": len(wins), "losses": len(losses), "breakevens": count - len(wins) - len(losses),
        "win_rate": Decimal(len(wins)) / count if count else None,
        "loss_rate": Decimal(len(losses)) / count if count else None,
        "average_win": sum(wins) / len(wins) if wins else None,
        "average_loss": sum(losses) / len(losses) if losses else None,
        "expectancy": net / count if count else None,
        "profit_factor": sum(wins) / -sum(losses) if losses else None,
        "average_r": sum(multiples) / count if count and len(multiples) == count else None,
        "maximum_wins": best_win, "maximum_losses": best_loss,
        "closed_trade_cash_drawdown": drawdown(opening, closed_samples),
        "end_of_day_equity_drawdown": drawdown(opening, eod),
        "intraday_mark_to_market_drawdown": None,
        "capital_exposure": None, "mae": None, "mfe": None, "sharpe": None, "sortino": None,
        "expectancy_interval": None,
    }
