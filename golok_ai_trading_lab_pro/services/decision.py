"""Deterministic, fail-closed gates for experimental candidates."""

GATES = {
    "G01": "Source eligibility", "G02": "Instrument eligibility", "G03": "Session validity",
    "G04": "Candle completeness", "G05": "Required freshness", "G06": "Research inputs",
    "G07": "Strategy implementation", "G08": "Mode-specific strategy validation", "G09": "Cost availability",
    "G10": "Position sizing", "G11": "Independent risk", "G12": "Decision expiry",
    "G13": "Evidence integrity", "G14": "Research mode restriction",
}


def evaluate(checks, *, mode, context=None):
    results = {}
    for key, name in GATES.items():
        evidence = checks.get(key)
        if isinstance(evidence, tuple):
            observed, threshold, passed = evidence
            passed = passed is True
        else:
            observed, threshold, passed = evidence, True, evidence is True
        if key == "G14":
            passed = passed and mode in ("synthetic_replay", "historical_contract_replay", "authorized_historical_replay")
        results[key] = {**(context or {}), "id": key, "label": name, "required_evidence": name, "observed": observed,
                        "threshold": threshold, "passed": passed, "status": "PASSED" if passed else "FAILED",
                        "reason": "SATISFIED" if passed else "EVIDENCE_VETO", "mode": mode}
    allowed = all(result["passed"] for result in results.values())
    return {"state": "SIMULATION_CANDIDATE" if allowed else "NO_TRADE", "gates": results,
            "financial_validation": "NOT_RUN", "live_actionability": "BLOCKED"}
