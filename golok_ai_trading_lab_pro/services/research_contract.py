"""Common evidence envelope for the original research capability inventory."""

VERSION = "r01-research-evidence-1"
CAPABILITIES = {
    "RE-01": "Technical analysis", "RE-02": "Fundamental analysis", "RE-03": "Price action",
    "RE-04": "Candlestick patterns", "RE-05": "Volume intelligence", "RE-06": "Support and resistance",
    "RE-07": "Breakout detection", "RE-08": "False breakout detection", "RE-09": "Market trend analysis",
    "RE-10": "Sector performance and rotation", "RE-11": "Benchmark index", "RE-12": "Global context",
    "RE-13": "Financial news and events", "RE-14": "Institutional activity proxies",
    "RE-15": "Historical pattern analysis", "RE-16": "Statistical probability estimation",
    "RE-17": "Liquidity", "RE-18": "Volatility", "RE-19": "Momentum", "RE-20": "Abnormal activity",
    "RE-21": "Entry optimization", "RE-22": "Stop-loss optimization", "RE-23": "Target optimization",
    "RE-24": "Historical strategy performance", "RE-25": "Net expected profit and risk validation",
}
PREREQUISITES = {
    "RE-02": "Authorized point-in-time fundamentals", "RE-10": "Authorized point-in-time sector panel",
    "RE-11": "Authorized aligned benchmark candles", "RE-12": "Authorized aligned global observations",
    "RE-13": "Authorized timestamped news or event records", "RE-14": "Authorized ownership or flow observations",
    "RE-16": "Independent authorized training and evaluation samples",
    "RE-21": "Causal strategy replay", "RE-22": "Causal strategy replay", "RE-23": "Target policy experiment",
    "RE-24": "Reconciled portfolio report", "RE-25": "Versioned tariff and passing risk checks",
}


def snapshot(context, core, supplemental, durations):
    records = {}
    for key, name in CAPABILITIES.items():
        evidence = core.get(key, supplemental.get(key))
        required = PREREQUISITES.get(key, "Validated ordered OHLCV")
        status = "WORKFLOW_REQUIRED" if key >= "RE-21" else "INPUT_UNAVAILABLE"
        finding = evidence.get("finding") if evidence else None
        warning = (evidence.get("quality_warning") or evidence.get("warning")) if evidence else None
        records[key] = {
            **context, "engine_id": key, "name": name, "engine_version": evidence.get("version") if evidence else None,
            "required_inputs": [required], "available_inputs": {"ohlcv_count": context["ohlcv_count"]},
            "finding": finding, "supporting_metrics": evidence or {}, "contradictory_evidence": [warning] if warning else [],
            "missing_inputs": [] if finding is not None else [required],
            "quality_warnings": [warning] if warning else [], "applicable_strategies": [],
            "execution_duration_ms": durations.get(key) if key in supplemental else (
                evidence.get("snapshot_duration_ms") if evidence else None),
            "execution_duration_scope": "engine" if key in durations else (
                "shared_snapshot" if evidence and evidence.get("snapshot_duration_ms") is not None else None),
            "status": evidence.get("status", status) if evidence else status,
        }
    return {"version": VERSION, "engines": records}
