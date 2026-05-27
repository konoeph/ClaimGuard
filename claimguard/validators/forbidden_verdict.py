from claimguard.core.claim import Claim
from claimguard.core.evidence import Evidence
from claimguard.core.policy import ClaimTypePolicy
from claimguard.core.result import Violation
from claimguard.core.tool_result import ToolResult


DETERMINISTIC_VERDICTS = {
    "pass",
    "fail",
    "yes",
    "no",
    "true",
    "false",
    "compliant",
    "non_compliant",
    "valid",
    "invalid",
}


def validate_forbidden_rules(
    claim: Claim,
    evidence_by_id: dict[str, Evidence],
    tool_results_by_id: dict[str, ToolResult],
    claim_policy: ClaimTypePolicy,
) -> list[Violation]:
    violations: list[Violation] = []

    for rule in claim_policy.forbidden:
        if rule == "answer_without_citation" and not claim.evidence_refs:
            violations.append(
                Violation(
                    claim_id=claim.id,
                    type="missing_citation",
                    message="Claim is not bound to any evidence citation.",
                    required="evidence_refs",
                    found=0,
                )
            )
        elif rule == "numeric_claim_without_tool" and not claim.tool_result_refs:
            violations.append(
                Violation(
                    claim_id=claim.id,
                    type="forbidden_verdict",
                    message="Numeric claim is not bound to any tool result.",
                    required="tool_result_refs",
                    found=0,
                    details={"rule": rule},
                )
            )
        elif rule == "unsupported_pass_fail" and _is_unsupported_pass_fail(claim):
            violations.append(
                Violation(
                    claim_id=claim.id,
                    type="unsupported_verdict",
                    message="Deterministic verdict is not bound to evidence.",
                    required="evidence_refs",
                    found=0,
                    details={"rule": rule},
                )
            )
        elif rule == "use_model_memory_as_authority" and _uses_model_memory(
            claim, evidence_by_id
        ):
            violations.append(
                Violation(
                    claim_id=claim.id,
                    type="forbidden_evidence",
                    message="Claim relies on model memory as authority.",
                    details={"rule": rule},
                )
            )

    return violations


def _is_unsupported_pass_fail(claim: Claim) -> bool:
    if claim.verdict is None:
        return False
    return (
        claim.verdict.strip().lower() in DETERMINISTIC_VERDICTS
        and not claim.evidence_refs
    )


def _uses_model_memory(claim: Claim, evidence_by_id: dict[str, Evidence]) -> bool:
    return any(
        evidence_by_id[ref].type == "model_memory"
        for ref in claim.evidence_refs
        if ref in evidence_by_id
    )

