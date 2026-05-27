from claimguard.core.claim import Claim
from claimguard.core.evidence import Evidence
from claimguard.core.policy import ClaimTypePolicy
from claimguard.core.result import Violation


def validate_required_evidence(
    claim: Claim,
    evidence_by_id: dict[str, Evidence],
    claim_policy: ClaimTypePolicy,
) -> list[Violation]:
    violations: list[Violation] = []
    referenced_evidence = [
        evidence_by_id[ref] for ref in claim.evidence_refs if ref in evidence_by_id
    ]

    for requirement in claim_policy.required_evidence:
        found = sum(
            1 for evidence in referenced_evidence if evidence.type == requirement.type
        )
        if found < requirement.min_count:
            violations.append(
                Violation(
                    claim_id=claim.id,
                    type="missing_required_evidence",
                    message=(
                        f"Claim requires at least {requirement.min_count} "
                        f"evidence item(s) of type '{requirement.type}'."
                    ),
                    required=requirement.type,
                    found=found,
                    refs=claim.evidence_refs,
                )
            )

    return violations

