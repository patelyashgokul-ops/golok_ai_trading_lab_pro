"""Reconcile completed virtual trades and report explicitly sampled drawdowns."""

from datetime import datetime
from decimal import Decimal
from bisect import bisect_left, bisect_right
from statistics import median


VERSION = "p09-performance-2"
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


def mark_portfolio(result, series):
    """Use frozen synthetic close marks, with cash after modeled events at each timestamp."""
    trades = result["trades"]
    positions = []
    for trade in trades:
        started = datetime.fromisoformat(trade["time"])
        ended = datetime.fromisoformat(trade["exit_time"])
        positions.append((trade["asset"], started, ended, trade["quantity"], amount(trade["entry"]), amount(trade["exit"])))
    samples = sorted({bar.close_time for bars in series.values() for bar in bars})
    indexed = {key: {bar.close_time: bar.close for bar in bars} for key, bars in series.items()}
    ledger = iter(sorted((datetime.fromisoformat(row["time"]), amount(row["delta"])) for row in result["ledger"]))
    pending = next(ledger, None)
    cash = amount(result["initial_cash"])
    equity_samples, exposure = [], []
    for timestamp in samples:
        while pending and pending[0] <= timestamp:
            cash += pending[1]
            pending = next(ledger, None)
        live = [(asset, quantity) for asset, start, end, quantity, _entry, _exit in positions
                if start <= timestamp < end]
        if any(timestamp not in indexed[asset] for asset, _quantity in live):
            return None
        outstanding = sum(indexed[asset][timestamp] * quantity for asset, quantity in live)
        equity_samples.append((timestamp, cash + outstanding))
        if cash + outstanding > 0:
            exposure.append(outstanding / (cash + outstanding))
    if not equity_samples or pending or equity_samples[-1][1] != amount(result["ending_cash"]):
        return None
    excursions = []
    for asset, start, end, quantity, entry, exit_price in positions:
        # Exit-bar order is unknown. Use only completed interior bars and the known exit.
        closes = [bar.close for bar in series[asset] if start < bar.close_time < end]
        moves = [(price - entry) * quantity for price in [entry, *closes, exit_price]]
        excursions.append((min(moves), max(moves)))
    return {
        "intraday_mark_to_market_drawdown": drawdown(amount(result["initial_cash"]), equity_samples),
        "capital_exposure": sum(exposure) / len(exposure) if exposure else None,
        "mae": min((values[0] for values in excursions), default=None),
        "mfe": max((values[1] for values in excursions), default=None),
        "mark_samples": len(equity_samples),
    }


def train_target_cap(result, series):
    """Fit a conservative price fraction from completed training trades."""
    marks = {asset: ([bar.close_time for bar in bars], bars) for asset, bars in series.items()}
    fractions = []
    sessions = set()
    for trade in result["trades"]:
        if trade["asset"] not in marks:
            return {"status": "INPUT_UNAVAILABLE", "observations": 0, "sessions": 0, "fraction": None}
        times, bars = marks[trade["asset"]]
        start = datetime.fromisoformat(trade["time"])
        end = datetime.fromisoformat(trade["exit_time"])
        entry, exit_price = amount(trade["entry"]), amount(trade["exit"])
        # The modeled exit is known. Highs from its candle may occur after the exit.
        interior = bars[bisect_right(times, start):bisect_left(times, end)]
        high_mark = max(entry, exit_price, *(bar.close for bar in interior))
        fractions.append(high_mark / entry - 1)
        sessions.add(start.date())
    result = {"status": "INSUFFICIENT_TRAINING", "observations": len(fractions),
              "sessions": len(sessions), "fraction": None}
    if len(fractions) >= 2 and len(sessions) >= 2:
        cap = min(median(fractions), Decimal(".10"))
        if cap > 0:
            result.update(status="FITTED", fraction=cap)
    return result


def summarize(result, *, marks=None):
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
    daily_returns = [amount(point["return"]) for point in result["days"] if point.get("return") is not None]
    sharpe = sortino = None
    if len(daily_returns) >= 20:
        mean = sum(daily_returns) / len(daily_returns)
        variance = sum((value - mean) ** 2 for value in daily_returns) / (len(daily_returns) - 1)
        downside = sum(min(value, ZERO) ** 2 for value in daily_returns) / len(daily_returns)
        annualized = Decimal(252).sqrt() * mean
        sharpe = annualized / variance.sqrt() if variance else None
        sortino = annualized / downside.sqrt() if downside else None
    metrics = {
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
        "capital_exposure": None, "mae": None, "mfe": None, "sharpe": sharpe, "sortino": sortino,
        "expectancy_interval": None,
    }
    if marks:
        metrics.update(marks)
    return metrics
