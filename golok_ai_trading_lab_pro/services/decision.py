"""Deterministic, fail-closed gates for experimental candidates."""

GATES = {
    "G01": "Source eligibility", "G02": "Instrument eligibility", "G03": "Session validity",
    "G04": "Candle completeness", "G05": "Required freshness", "G06": "Research inputs",
    "G07": "Strategy implementation", "G08": "Mode-specific strategy validation", "G09": "Cost availability",
    "G10": "Position sizing", "G11": "Independent risk", "G12": "Decision expiry",
    "G13": "Evidence integrity", "G14": "Research mode restriction",
}


def evaluate(checks, *, mode):
    results = {key: {"label": name, "passed": checks.get(key) is True}
               for key, name in GATES.items()}
    results["G14"]["passed"] &= mode == "synthetic_replay"
    allowed = all(result["passed"] for result in results.values())
    return {"state": "SIMULATION_CANDIDATE" if allowed else "NO_TRADE", "gates": results}
