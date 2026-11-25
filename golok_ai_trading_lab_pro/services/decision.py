"""Deterministic, fail-closed gates for experimental candidates."""

import re
from dataclasses import asdict
from hashlib import sha256

from .backtest import canonical

GATES = {
    "G01": "Source eligibility", "G02": "Instrument eligibility", "G03": "Session validity",
    "G04": "Candle completeness", "G05": "Required freshness", "G06": "Research inputs",
    "G07": "Strategy implementation", "G08": "Mode-specific strategy validation", "G09": "Cost availability",
    "G10": "Position sizing", "G11": "Independent risk", "G12": "Decision expiry",
    "G13": "Evidence integrity", "G14": "Research mode restriction",
}
RESEARCH_MODES = frozenset({"synthetic_replay", "historical_contract_replay",
                            "authorized_historical_replay", "prospective_fixture"})
PROVENANCE_KEYS = frozenset({"evaluated_at", "strategy_version", "dataset_version", "source_record",
                             "observation_sha256", "decision_input_sha256", "execution_scope"})


def observation_digest(bars):
    return sha256(canonical([asdict(bar) for bar in bars]).encode()).hexdigest()


def valid_digest(value):
    return isinstance(value, str) and re.fullmatch(r"[a-f0-9]{64}", value) is not None


def evidence_passed(value):
    return value is True or (isinstance(value, tuple) and len(value) == 3 and value[2] is True)


def evaluate(checks, *, mode, context=None, require_provenance=False):
    context = {key: value for key, value in (context or {}).items() if key in PROVENANCE_KEYS}
    results = {}
    for key, name in GATES.items():
        evidence = checks.get(key)
        passed = evidence_passed(evidence)
        if isinstance(evidence, tuple) and len(evidence) == 3:
            observed, threshold, _passed = evidence
        else:
            observed, threshold = evidence, True
        reason = "SATISFIED" if passed else "MISSING_EVIDENCE" if evidence is None else "EVIDENCE_VETO"
        if key == "G13" and require_provenance and not (
                valid_digest(context.get("dataset_version")) and valid_digest(context.get("observation_sha256"))):
            passed, reason = False, "INVALID_PROVENANCE"
        if key == "G14":
            if mode not in RESEARCH_MODES:
                passed, reason = False, "UNSUPPORTED_MODE"
        results[key] = {**context, "id": key, "label": name, "required_evidence": name, "observed": observed,
                        "threshold": threshold, "passed": passed, "status": "PASSED" if passed else "FAILED",
                        "reason": reason, "mode": mode}
    allowed = all(result["passed"] for result in results.values())
    return {"state": "SIMULATION_CANDIDATE" if allowed else "NO_TRADE", "gates": results,
            "financial_validation": "NOT_RUN", "live_actionability": "BLOCKED"}
