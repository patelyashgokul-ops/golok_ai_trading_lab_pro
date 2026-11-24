"""Bounded synthetic-only portfolio replay with one fee-aware capital ledger."""

from dataclasses import asdict, dataclass, replace
from datetime import timedelta
from decimal import Decimal
from itertools import groupby

from . import decision, eligibility, simulation, strategies, targets

MAX_INSTRUMENTS = 16
MAX_BARS = 12000


@dataclass(frozen=True)
class PortfolioPolicy:
    daily_loss: Decimal = Decimal(".01")
    daily_entries: int = 3
    consecutive_losses: int = 2
    max_positions: int = 4


@dataclass(frozen=True)
class Series:
    key: str
    exchange: str
    tick: Decimal
    bars: tuple
    sessions: dict
    origin: str = "synthetic"
    quarantined: bool = False


def _events(series, starts, ends, seconds, *, historical=False):
    events = []
    for asset in series:
        if (historical and (asset.origin != ("historical_contract" if historical == "fixture" else "authorized_historical")
                            or asset.quarantined)
                or not historical and not eligibility.evaluate(
                    asset.origin, "synthetic_replay", quarantined=asset.quarantined)[1]):
            raise ValueError("Synthetic portfolio source eligibility failed.")
        if asset.exchange not in ("NSE", "BSE") or not simulation.finite(asset.tick) or asset.tick <= 0:
            raise ValueError("Each instrument requires a supported exchange and a positive tick.")
        expected = []
        for offset in range((ends - starts).days + 1):
            day = starts + timedelta(days=offset)
            session = asset.sessions.get(day)
            if not session or session.kind not in ("regular", "closed") or session.segments:
                raise ValueError("Requested coverage needs explicit regular or closed session dates.")
            slots = session.slots(seconds)
            if slots and session.exit_cutoff not in {end for _, end in slots}:
                raise ValueError("Exit cutoff needs a session-grid observation.")
            expected.extend((start, end, session) for start, end in slots)
        if len(expected) != len(asset.bars):
            raise ValueError("Incomplete session coverage; no portfolio result was priced.")
        for bar, (start, end, session) in zip(asset.bars, expected):
            values = (bar.open, bar.high, bar.low, bar.close)
            if (
                (bar.open_time, bar.close_time) != (start, end)
                or (not historical and bar.available_at != end)
                or (historical and not end <= bar.available_at <= session.closing)
                or not all(simulation.finite(p) and p > 0 and p % asset.tick == 0 for p in values)
                or not (bar.low <= min(bar.open, bar.close) <= max(bar.open, bar.close) <= bar.high)
                or type(bar.volume) is not int or bar.volume < 0
            ):
                raise ValueError("Replay requires a complete tick-aligned grid and compatible publication timestamps.")
            # Complete closes before new opens at the same timestamp. Stable key breaks ties.
            events.extend(((start, 1, asset.key, bar, session), (end, 0, asset.key, bar, session)))
            if historical:
                events.append((bar.available_at, 2, asset.key, bar, session))
    return sorted(events, key=lambda event: event[:3])


def replay(series, starts, ends, seconds, codes, costs, *, capital=Decimal("50000"),
           portfolio_policy=PortfolioPolicy(), target_policy="structure"):
    return _replay(series, starts, ends, seconds, codes, costs, capital=capital,
                   portfolio_policy=portfolio_policy, target_policy=target_policy, historical=False)


def _replay(series, starts, ends, seconds, codes, costs, *, capital, portfolio_policy, target_policy, historical):
    if (not 1 <= len(series) <= MAX_INSTRUMENTS or len({asset.key for asset in series}) != len(series)
            or sum(len(asset.bars) for asset in series) > MAX_BARS
            or not starts <= ends < starts + timedelta(days=31) or seconds not in (60, 180, 300, 900)
            or not codes or len(set(codes)) != len(codes) or not set(codes) <= strategies.REGISTRY.keys()
            or target_policy not in targets.POLICIES or not simulation.finite(capital) or capital <= 0):
        raise ValueError("Use bounded, distinct synthetic instruments, known strategies and positive virtual capital.")
    if (not simulation.finite(portfolio_policy.daily_loss) or not 0 < portfolio_policy.daily_loss <= 1
            or any(type(value) is not int or value <= 0 for value in (
                portfolio_policy.daily_entries, portfolio_policy.consecutive_losses, portfolio_policy.max_positions))):
        raise ValueError("Invalid portfolio risk policy.")
    events = _events(series, starts, ends, seconds, historical=historical)
    mode = {"fixture": "historical_contract_replay", "authorized": "authorized_historical_replay"}.get(
        historical, "synthetic_replay")
    assets = {asset.key: asset for asset in series}
    cash = capital
    day = None
    daily_open = capital
    daily_realized = Decimal(0)
    entries = streak = 0
    suspended = False
    histories, pending, positions = {}, {}, {}
    trades, decisions, ledger, daily = [], [], [], []

    def evaluate_candidate(key, when, bar, session, candidate, *, record):
        nonlocal cash, entries
        asset = assets[key]
        code, observed, stop = candidate
        valid_time = (observed.available_at < when <= observed.available_at + timedelta(seconds=seconds)
                      and when < min(session.entry_cutoff, session.exit_cutoff))
        exposure = sum(position["loss"] for position in positions.values())
        risk_room = max(Decimal(0), daily_open * portfolio_policy.daily_loss + min(daily_realized, 0) - exposure)
        levels, target_reason = targets.levels(histories[key], bar.open, stop, target_policy, when, session.exit_cutoff)
        target = levels[0] if levels else None
        if target is not None and target_policy == "atr_barrier":
            target = target // asset.tick * asset.tick
        risk_capital = min(cash, daily_open)
        risk = replace(simulation.RiskPolicy(), capital=risk_capital)
        sizing = (simulation.size_long(bar.open, stop, target, asset.tick, observed.volume, session.day,
                                       asset.exchange, costs, risk) if target is not None
                  else simulation.Sizing(0, target_reason))
        rank = targets.rank(sizing, observed.volume)
        if not record:
            return rank
        try:
            costs.fees(session.day, asset.exchange, "buy", bar.open, 1)
            costs.fees(session.day, asset.exchange, "sell", bar.open, 1)
            cost_available = True
        except ValueError:
            cost_available = False
        independent = bool(sizing.quantity) and not suspended and entries < portfolio_policy.daily_entries and (
            len(positions) < portfolio_policy.max_positions and key not in positions
            and sizing.loss <= risk_room and daily_realized > -daily_open * portfolio_policy.daily_loss
        )
        source, eligible = eligibility.evaluate(asset.origin, "synthetic_replay", quarantined=asset.quarantined)
        if historical:
            source = "VERIFIED_CONTRACT_FIXTURE" if historical == "fixture" else "AUTHORIZED_HISTORICAL_INPUT"
            eligible = not asset.quarantined
        history = histories[key]
        checks = {
            "G01": (source, "eligible synthetic source", eligible),
            "G02": (asset.exchange, "NSE or BSE; positive tick", asset.exchange in ("NSE", "BSE") and asset.tick > 0),
            "G03": (session.kind, "regular", session.kind == "regular"),
            "G04": (len(history), "validated complete replay grid", bool(history) and observed in history),
            "G05": (observed.available_at, "strictly before execution", observed.available_at < when),
            "G06": (target_reason, "causal level and entry within 1% of signal close",
                    target is not None and stop < bar.open <= observed.close * Decimal("1.01")),
            "G07": (code, "registered strategy", code in strategies.REGISTRY),
            "G08": (asset.origin, "research-mode permission only" if historical else "synthetic experiment permission only",
                    eligible and code in strategies.REGISTRY),
            "G09": (cost_available, "complete hypothetical tariff", cost_available),
            "G10": ((sizing.quantity, sizing.reward, sizing.loss), "positive quantity and at least 2:1 net", sizing.quantity > 0),
            "G11": ((risk_room, entries, suspended), "shared risk and cash available; no duplicate position", independent),
            "G12": (when - observed.available_at, "later open within one interval and cutoff", valid_time),
            "G13": (observed.close_time, "publication verified" if historical else "validated source observation available at close",
                    (observed.available_at >= observed.close_time if historical else observed.available_at == observed.close_time)
                    and observed in history),
            "G14": (source, "historical contract simulation only" if historical else "synthetic simulation only", eligible),
        }
        outcome = decision.evaluate(checks, mode=mode, context={
            "evaluated_at": when, "strategy_version": strategies.VERSION, "dataset_version": asset.key,
            "source_record": observed.close_time})
        decisions.append({"asset": key, "strategy": code, "time": when, "sizing": sizing.reason,
                          "target_policy": target_policy, "target": target, "rank": rank,
                          "outcome_reason": "SELECTED" if outcome["state"] == "SIMULATION_CANDIDATE" else "GATE_VETO",
                          **outcome})
        if outcome["state"] != "SIMULATION_CANDIDATE":
            return
        quantity = sizing.quantity
        buy_fees = sum(costs.fees(session.day, asset.exchange, "buy", bar.open, quantity).values())
        debit = bar.open * quantity + buy_fees
        if debit > cash:
            raise ArithmeticError("Cash invariant violated.")
        cash -= debit
        entries += 1
        positions[key] = {"strategy": code, "entry": bar.open, "quantity": quantity, "stop": stop, "target": target,
                          "loss": sizing.loss, "entry_debit": debit, "buy_fees": buy_fees, "time": when}
        ledger.append({"asset": key, "time": when, "kind": "RESERVE_AND_FILL", "delta": -debit, "cash": cash})

    def close(key, when, price, reason):
        nonlocal cash, daily_realized, streak, suspended
        position = positions.pop(key)
        qty = position["quantity"]
        sell_fees = sum(costs.fees(day, assets[key].exchange, "sell", price, qty).values())
        credit = price * qty - sell_fees
        net = credit - position["entry_debit"]
        daily_realized += net
        cash += credit
        if cash < 0:
            raise ValueError("The simulated exit cannot fund its fees from virtual cash.")
        streak = streak + 1 if net < 0 else 0
        suspended |= streak >= portfolio_policy.consecutive_losses
        trades.append({"asset": key, **position, "exit": price, "exit_time": when, "reason": reason,
                       "gross": (price - position["entry"]) * qty, "fees": position["buy_fees"] + sell_fees, "net": net})
        ledger.append({"asset": key, "time": when, "kind": "CLOSE", "delta": credit, "cash": cash})

    def expire_candidates():
        for key, candidates in sorted(pending.items()):
            for code, bar, _ in candidates:
                outcome = decision.evaluate({"G12": ("no later open", "strictly later open", False)},
                                            mode=mode, context={"evaluated_at": bar.available_at,
                                            "dataset_version": key, "source_record": bar.close_time,
                                            "strategy_version": strategies.VERSION})
                decisions.append({"asset": key, "strategy": code, "time": bar.available_at,
                                  "sizing": "NO_LATER_OPEN", **outcome})

    for (when, phase), grouped in groupby(events, key=lambda event: event[:2]):
        batch = list(grouped)
        session = batch[0][4]
        if session.day != day:
            if day is not None:
                expire_candidates()
                daily.append({"date": day, "cash": cash, "return": cash / daily_open - 1 if daily_open else None})
            if positions:
                raise ValueError("Unresolved overnight position; no fictional closing value.")
            day, daily_open, daily_realized, entries = session.day, cash, Decimal(0), 0
            histories, pending = {}, {}
        if phase == 1:
            competing = []
            for _, _, key, bar, session in batch:
                position = positions.get(key)
                if position and bar.open <= position["stop"]:
                    close(key, when, bar.open, "GAP_STOP")
            for _, _, key, bar, session in batch:
                candidates = pending.get(key)
                if candidates and candidates[0][1].available_at < when:
                    for candidate in pending.pop(key):
                        rank = evaluate_candidate(key, when, bar, session, candidate, record=False)
                        competing.append((rank, key, candidate[0], bar, session, candidate))
            competing.sort(key=lambda entry: (entry[1], entry[2]))
            competing.sort(key=lambda entry: entry[0], reverse=True)
            for _, key, _, bar, session, candidate in competing:
                evaluate_candidate(key, when, bar, session, candidate, record=True)
            continue
        for _, _, key, bar, session in batch:
            position = positions.get(key)
            if position and phase == 0:
                if bar.low <= position["stop"]:
                    close(key, when, position["stop"], "STOP_FIRST")
                elif bar.high > position["target"]:
                    close(key, when, position["target"], "TRADE_THROUGH_TARGET")
                elif when >= session.exit_cutoff or when - position["time"] >= timedelta(seconds=12 * seconds):
                    close(key, when, bar.close, "TIME_EXIT")
            if historical and phase == 0:
                continue
            history = histories.setdefault(key, [])
            history.append(bar)
            if key not in positions and key not in pending and when < session.entry_cutoff:
                candidates = [(code, bar, stop) for code in sorted(codes)
                              if (stop := strategies.REGISTRY[code].signal(history, session)) is not None]
                if candidates:
                    pending[key] = candidates
    if positions:
        raise ValueError("Unresolved closing observation.")
    if day is not None:
        expire_candidates()
        daily.append({"date": day, "cash": cash, "return": cash / daily_open - 1 if daily_open else None})
    peak = capital
    drawdown = Decimal(0)
    for row in daily:
        peak = max(peak, row["cash"])
        drawdown = max(drawdown, peak - row["cash"])
    net = cash - capital
    return {
        "scope": {"fixture": "HISTORICAL_CONTRACT_FIXTURE_ONLY", "authorized": "AUTHORIZED_HISTORICAL_SIMULATION"}.get(
            historical, "SYNTHETIC_SOFTWARE_ONLY"),
        "initial_cash": capital, "ending_cash": cash,
        "policy": asdict(portfolio_policy), "trades": trades, "ledger": ledger, "decisions": decisions, "days": daily,
        "suspended": suspended, "net": net, "gross": sum((t["gross"] for t in trades), Decimal(0)),
        "fees": sum((t["fees"] for t in trades), Decimal(0)), "daily_closed_drawdown": drawdown,
    }
