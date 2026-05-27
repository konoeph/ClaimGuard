from claimguard.core.claim import Claim
from claimguard.core.evidence import Evidence
from claimguard.core.result import Violation
from claimguard.core.tool_result import ToolResult


def validate_citation_binding(
    claim: Claim,
    evidence_by_id: dict[str, Evidence],
    tool_results_by_id: dict[str, ToolResult],
) -> list[Violation]:
    violations: list[Violation] = []

    missing_evidence_refs = [
        ref for ref in claim.evidence_refs if ref not in evidence_by_id
    ]
    if missing_evidence_refs:
        violations.append(
            Violation(
                claim_id=claim.id,
                type="invalid_evidence_ref",
                message="Claim references evidence IDs that were not provided.",
                refs=missing_evidence_refs,
            )
        )

    missing_tool_refs = [
        ref for ref in claim.tool_result_refs if ref not in tool_results_by_id
    ]
    if missing_tool_refs:
        violations.append(
            Violation(
                claim_id=claim.id,
                type="invalid_tool_result_ref",
                message="Claim references tool result IDs that were not provided.",
                refs=missing_tool_refs,
            )
        )

    return violations

