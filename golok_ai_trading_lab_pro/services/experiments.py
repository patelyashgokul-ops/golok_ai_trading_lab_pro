"""Bounded, reproducible sequential synthetic account replay."""

import hashlib
import json
from collections import defaultdict
from dataclasses import asdict, replace
from datetime import date, timedelta
from decimal import Decimal

from . import backtest, calendar, simulation

VERSION = "ST-01/multi-3"
MAX_DAYS = 31
MAX_BARS = 4000


def read_tariffs(raw):
    if not raw or len(raw) > 96 * 1024:
        raise ValueError("Supply a tariff JSON document up to 96 KiB.")
    try:
        entries = json.loads(raw, parse_float=Decimal)
        if not isinstance(entries, list) or not 1 <= len(entries) <= 100:
            raise ValueError
        rules = []
        for entry in entries:
            rule = dict(entry)
            rule["starts"] = date.fromisoformat(rule["starts"])
            rule["ends"] = date.fromisoformat(rule["ends"]) if rule.get("ends") else None
            for field in ("amount", "minimum", "maximum"):
                if rule.get(field) is not None:
                    rule[field] = Decimal(rule[field])
            if rule.get("verification", "hypothetical") != "hypothetical":
                raise ValueError
            rules.append(simulation.Tariff(**rule))
        return simulation.CostSchedule(rules)
    except (KeyError, TypeError, ValueError, ArithmeticError, RecursionError):
        raise ValueError("Invalid hypothetical tariff document.") from None


def simulate(bars, sessions, starts, ends, exchange, seconds, tick, costs, source, risk):
    if not starts <= ends < starts + timedelta(days=MAX_DAYS) or len(bars) > MAX_BARS:
        raise ValueError("Experiments support at most 31 dates and 4,000 observations.")
    by_day = defaultdict(list)
    for bar in bars:
        day = bar.close_time.astimezone(calendar.IST).date()
        if not starts <= day <= ends:
            raise ValueError("Observation outside the frozen experiment dates.")
        by_day[day].append(bar)
    specification = {
        "implementation": VERSION, "starts": starts, "ends": ends, "exchange": exchange, "interval": seconds,
        "tick": tick, "source": source, "risk": asdict(risk), "tariffs": [asdict(t) for t in costs.tariffs],
        "strategy": asdict(backtest.OpeningRangeVersion()), "origin": "synthetic",
        "input_digest": hashlib.sha256(backtest.canonical([asdict(bar) for bar in bars]).encode()).hexdigest(),
    }
    equity = [risk.capital]
    daily = []
    trades = []
    candidates = 0
    peak = risk.capital
    drawdown = Decimal(0)
    loss_streak = longest_loss_streak = 0
    status = "completed"
    for offset in range((ends - starts).days + 1):
        day = starts + timedelta(days=offset)
        if loss_streak >= 2:
            status = "risk_suspended"
            daily.append({"day": day, "status": "RISK_SUSPENDED", "reason": "Two consecutive realized losses."})
            break
        session = sessions.get(day)
        if session and session.kind == "closed":
            daily.append({"day": day, "status": "CLOSED"})
            continue
        try:
            if not session:
                raise ValueError("Missing calendar coverage.")
            if session.kind != "regular" or session.segments:
                raise ValueError("This strategy version requires a single continuous regular session.")
            if equity[-1] <= 0:
                raise ValueError("Virtual capital exhausted.")
            result = backtest.replay(by_day.get(day, []), session, exchange, seconds, tick, costs, source=source,
                                     partition="validation", origin="synthetic", risk=replace(risk, capital=equity[-1]))
        except ValueError as exc:
            # Capital after this point is unknowable. Keep the preceding results without simulating past the gap.
            status = "unresolved"
            daily.append({"day": day, "status": "UNRESOLVED", "reason": str(exc)})
            break
        daily.append({"day": day, "status": "REPLAYED", "digest": result["experiment"], "candidates": result["candidates"]})
        candidates += len(result["candidates"])
        trade = result["trade"]
        if trade:
            trades.append({"day": day, **trade})
            loss_streak = loss_streak + 1 if trade["net"] < 0 else 0
            longest_loss_streak = max(longest_loss_streak, loss_streak)
        ending = equity[-1] + (trade["net"] if trade else 0)
        equity.append(ending)
        peak = max(peak, ending)
        drawdown = max(drawdown, peak - ending)
    gross_wins = sum((row["net"] for row in trades if row["net"] > 0), Decimal(0))
    gross_losses = sum((-row["net"] for row in trades if row["net"] < 0), Decimal(0))
    net = sum((row["net"] for row in trades), Decimal(0))
    wins = sum(row["net"] > 0 for row in trades)
    losses = sum(row["net"] < 0 for row in trades)
    metrics = {
        "considered": candidates, "rejected": candidates - len(trades), "trades": len(trades),
        "wins": wins, "losses": losses, "neutral": len(trades) - wins - losses,
        "net": net if trades else None, "costs": sum((row["costs"] for row in trades), Decimal(0)),
        "net_per_trade": net / len(trades) if trades else None,
        "win_fraction": Decimal(wins) / len(trades) if trades else None,
        "profit_factor_net_trade": gross_wins / gross_losses if gross_losses else None,
        "max_drawdown_closed": drawdown, "consecutive_losses": longest_loss_streak, "equity_closed": equity,
        "turnover": sum(((row["entry"] + row["exit"]) * row["quantity"] for row in trades), Decimal(0)),
    }
    return {"specification": specification, "status": status,
            "requested_dates": (ends - starts).days + 1,
            "evaluated_dates": sum(row["status"] in ("CLOSED", "REPLAYED") for row in daily),
            "days": daily, "trades": trades, "metrics": metrics}
