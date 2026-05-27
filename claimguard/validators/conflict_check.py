from claimguard.core.claim import Claim
from claimguard.core.evidence import Evidence
from claimguard.core.result import Violation


def validate_conflicting_evidence(
    claim: Claim,
    evidence_by_id: dict[str, Evidence],
) -> list[Violation]:
    referenced = [
        evidence_by_id[ref] for ref in claim.evidence_refs if ref in evidence_by_id
    ]
    referenced_ids = {evidence.id for evidence in referenced}

    explicit_conflicts = []
    for evidence in referenced:
        conflicts_with = evidence.metadata.get("conflicts_with", [])
        if isinstance(conflicts_with, str):
            conflicts_with = [conflicts_with]
        for conflict_id in conflicts_with:
            if conflict_id in referenced_ids:
                explicit_conflicts.append((evidence.id, conflict_id))

    if explicit_conflicts:
        refs = sorted({item for pair in explicit_conflicts for item in pair})
        return [
            Violation(
                claim_id=claim.id,
                type="conflicting_evidence",
                message="Claim cites evidence items marked as conflicting.",
                refs=refs,
                details={"conflicts": explicit_conflicts},
            )
        ]

    grouped_values: dict[str, set[str]] = {}
    grouped_refs: dict[str, list[str]] = {}
    for evidence in referenced:
        conflict_group = evidence.metadata.get("conflict_group")
        conflict_value = evidence.metadata.get("conflict_value")
        if conflict_group is None or conflict_value is None:
            continue
        grouped_values.setdefault(str(conflict_group), set()).add(str(conflict_value))
        grouped_refs.setdefault(str(conflict_group), []).append(evidence.id)

    for conflict_group, values in grouped_values.items():
        if len(values) > 1:
            return [
                Violation(
                    claim_id=claim.id,
                    type="conflicting_evidence",
                    message="Claim cites evidence with incompatible conflict values.",
                    refs=grouped_refs[conflict_group],
                    details={"conflict_group": conflict_group, "values": sorted(values)},
                )
            ]

    return []

