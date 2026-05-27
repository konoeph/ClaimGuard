from claimguard import ClaimGuard, Policy


def test_missing_required_evidence_blocks_claim() -> None:
    policy = Policy.load("claimguard/policies/generic_compliance.yaml")

    result = ClaimGuard(policy).verify(
        claims=[
            {
                "id": "claim_1",
                "type": "compliance_judgement",
                "text": "This practice is compliant.",
                "verdict": "pass",
                "evidence_refs": ["ev_1"],
            }
        ],
        evidence=[
            {
                "id": "ev_1",
                "type": "source_fact",
                "content": "The vendor stores customer records for 30 days.",
            }
        ],
    )

    assert result.status == "blocked"
    assert result.claim_results[0].status == "insufficient_evidence"
    assert result.violations[0].type == "missing_required_evidence"
    assert result.violations[0].required == "regulation"

