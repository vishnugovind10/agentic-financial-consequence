"""Deterministic consequence binding: compare authorized intent with observed state."""

from datetime import datetime, timezone
from typing import Any

from .models import Decision, Evaluation, Result

CHECKS = ("authorization", "execution", "settlement", "liquidity", "reconciliation", "evidence", "consequence")


def _freshness(evidence: dict[str, Any], as_of: str) -> bool:
    try:
        observed = datetime.fromisoformat(evidence["observed_at"].replace("Z", "+00:00"))
        reference = datetime.fromisoformat(as_of.replace("Z", "+00:00"))
        if observed.tzinfo is None:
            observed = observed.replace(tzinfo=timezone.utc)
        if reference.tzinfo is None:
            reference = reference.replace(tzinfo=timezone.utc)
        age_days = (reference - observed).total_seconds() / 86400
        return 0 <= age_days <= evidence["max_age_days"]
    except (KeyError, TypeError, ValueError):
        return False


def evaluate(envelope: dict[str, Any]) -> Evaluation:
    """Evaluate a JSON-compatible envelope; missing or contradictory evidence abstains."""
    intent, authority = envelope["intent"], envelope["authority"]
    execution, observed = envelope["execution"], envelope["observed_state"]
    evidence = envelope["evidence"]
    reasons: list[str] = []
    auth_ok = (
        authority.get("decision") == "ALLOW"
        and intent.get("source") in authority.get("resources", [])
        and intent.get("amount", 0) > 0
        and intent.get("amount", 0) <= authority.get("amount_limit", -1)
    )
    checks: dict[str, Result] = {"authorization": Result.PASS if auth_ok else Result.FAIL}
    if not auth_ok:
        reasons.append("Intent is not covered by the recorded authority.")

    checks["execution"] = Result.PASS if execution.get("status") == "EXECUTED" else Result.ABSTAIN
    checks["settlement"] = _observed_check(observed, "settlement", "SETTLED")
    checks["liquidity"] = _observed_check(observed, "liquidity", "WITHIN_LIMIT")
    checks["reconciliation"] = _reconciliation(observed)
    checks["evidence"] = Result.PASS if _freshness(evidence, envelope["as_of"]) else Result.ABSTAIN
    if checks["evidence"] is Result.ABSTAIN:
        reasons.append("Required evidence is missing, future-dated, or stale at scenario as_of.")

    amount = execution.get("amount")
    consequence_ok = (
        amount == intent.get("amount")
        and execution.get("source") == intent.get("source")
        and execution.get("destination") == intent.get("destination")
        and execution.get("counterparty") == authority.get("counterparty")
        and observed.get("beneficial_owner") == authority.get("beneficial_owner")
        and observed.get("exposure", float("inf")) <= authority.get("exposure_limit", -1)
        and execution.get("source") in authority.get("resources", [])
    )
    checks["consequence"] = Result.PASS if consequence_ok else Result.FAIL
    if not consequence_ok:
        reasons.append("Observed economic consequence falls outside the authorized boundary.")

    values = set(checks.values())
    if Result.FAIL in values:
        decision = Decision.NO_GO
    elif Result.ABSTAIN in values:
        decision = Decision.ABSTAIN
    else:
        decision = Decision.GO
    return Evaluation(envelope.get("scenario", "unnamed"), checks, decision, tuple(reasons))


def _observed_check(observed: dict[str, Any], key: str, expected: str) -> Result:
    value = observed.get(key)
    if value is None or value in ("UNKNOWN", "PENDING"):
        return Result.ABSTAIN
    return Result.PASS if value == expected else Result.FAIL


def _reconciliation(observed: dict[str, Any]) -> Result:
    value = observed.get("reconciliation")
    if value in (None, "UNKNOWN", "PENDING", "MISMATCH_UNEXPLAINED"):
        return Result.ABSTAIN
    return Result.PASS if value == "MATCHED" else Result.FAIL
