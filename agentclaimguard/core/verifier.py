from collections.abc import Iterable

from agentclaimguard.core.claim import Claim
from agentclaimguard.core.evidence import Evidence
from agentclaimguard.core.policy import Policy
from agentclaimguard.core.result import (
    ClaimVerificationResult,
    ClaimStatus,
    VerificationResult,
    Violation,
)
from agentclaimguard.core.tool_result import ToolResult
from agentclaimguard.validators.citation_binding import validate_citation_binding
from agentclaimguard.validators.conflict_check import validate_conflicting_evidence
from agentclaimguard.validators.evidence_required import validate_required_evidence
from agentclaimguard.validators.forbidden_verdict import validate_forbidden_rules
from agentclaimguard.validators.tool_required import validate_required_tools


def verify_claims(
    claims: Iterable[Claim],
    evidence: Iterable[Evidence],
    tool_results: Iterable[ToolResult],
    policy: Policy,
) -> VerificationResult:
    evidence_by_id = {item.id: item for item in evidence}
    tool_results_by_id = {item.id: item for item in tool_results}

    claim_results: list[ClaimVerificationResult] = []
    all_violations: list[Violation] = []

    for claim in claims:
        claim_policy = policy.policy_for_claim_type(claim.type)
        violations: list[Violation] = []
        violations.extend(validate_citation_binding(claim, evidence_by_id, tool_results_by_id))
        violations.extend(validate_required_evidence(claim, evidence_by_id, claim_policy))
        violations.extend(validate_required_tools(claim, tool_results_by_id, claim_policy))
        violations.extend(validate_forbidden_rules(claim, evidence_by_id, tool_results_by_id, claim_policy))
        violations.extend(validate_conflicting_evidence(claim, evidence_by_id))

        if violations:
            fallback = policy.fallback_for_claim_type(claim.type)
            status = _status_from_violations(violations)
            claim_result = ClaimVerificationResult(
                claim_id=claim.id,
                status=status,
                violations=violations,
                safe_verdict=fallback.verdict,
                reason=fallback.reason,
            )
            all_violations.extend(violations)
        else:
            claim_result = ClaimVerificationResult(claim_id=claim.id, status="passed")

        claim_results.append(claim_result)

    status = "passed" if not all_violations else "blocked"
    return VerificationResult(
        status=status,
        claim_results=claim_results,
        violations=all_violations,
        safe_output=_safe_output(claim_results),
    )


def _status_from_violations(violations: list[Violation]) -> ClaimStatus:
    violation_types = {violation.type for violation in violations}
    if "conflicting_evidence" in violation_types:
        return "conflicting_evidence"
    if "required_tool_error" in violation_types:
        return "tool_error"
    if "missing_required_tool_result" in violation_types:
        return "tool_required"
    if {
        "missing_required_evidence",
        "missing_citation",
        "invalid_evidence_ref",
    } & violation_types:
        return "insufficient_evidence"
    return "blocked"


def _safe_output(
    claim_results: list[ClaimVerificationResult],
) -> dict[str, list[dict[str, str | None]]]:
    blocked = [
        {
            "claim_id": result.claim_id,
            "safe_verdict": result.safe_verdict,
            "reason": result.reason,
            "status": result.status,
        }
        for result in claim_results
        if result.status != "passed"
    ]
    return {"blocked_claims": blocked}

