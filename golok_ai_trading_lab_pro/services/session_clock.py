"""Classify the exchange phase from explicit session windows."""

from datetime import timedelta


def phase(session, at):
    if not session:
        return "blocked"
    if session.kind == "closed":
        return "closed"
    if at < session.opening:
        return "pre_market"
    if at >= session.closing:
        return "post_market"
    if not any(left <= at < right for left, right in session.windows()):
        return "maintenance"
    if at < min(session.opening + timedelta(minutes=5), session.closing):
        return "market_opening"
    return "intraday"
