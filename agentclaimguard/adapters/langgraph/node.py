from collections.abc import Mapping
from typing import Any

from pydantic import ValidationError

from agentclaimguard.core.policy import Policy
from agentclaimguard.core.result import VerificationResult
from agentclaimguard.core.runtime import AgentClaimGuard

from .types import EvidenceGuardNode, GuardRoute


_ROUTABLE_CLAIM_STATUSES: set[GuardRoute] = {
    "need_check",
    "insufficient_evidence",
    "conflicting_evidence",
}


def create_evidence_guard_node(
    policy: Policy,
    *,
    claims_key: str = "claims",
    evidence_key: str = "evidence",
    tool_results_key: str = "tool_results",
    result_key: str = "guard_result",
) -> EvidenceGuardNode:
    """Create a LangGraph-compatible node for AgentClaimGuard verification."""
    guard = AgentClaimGuard(policy=policy)

    def evidence_guard_node(state: Mapping[str, Any]) -> dict[str, VerificationResult]:
        result = guard.verify(
            claims=state.get(claims_key, []),
            evidence=state.get(evidence_key, []),
            tool_results=state.get(tool_results_key, []),
        )
        return {result_key: result}

    return evidence_guard_node


def route_by_guard_status(
    state: Mapping[str, Any],
    *,
    result_key: str = "guard_result",
) -> GuardRoute:
    result = _coerce_result(state.get(result_key))
    if result is None:
        return "need_check"

    if result.status == "passed":
        return "passed"

    claim_status = _first_non_passed_claim_status(result)
    if claim_status in _ROUTABLE_CLAIM_STATUSES:
        return claim_status

    return "blocked"


def _coerce_result(value: Any) -> VerificationResult | None:
    if value is None:
        return None
    if isinstance(value, VerificationResult):
        return value
    if isinstance(value, Mapping):
        try:
            return VerificationResult.model_validate(value)
        except ValidationError:
            return None
    return None


def _first_non_passed_claim_status(result: VerificationResult) -> str | None:
    for claim_result in result.claim_results:
        if claim_result.status != "passed":
            return claim_result.status
    return None
