from agentclaimguard import AgentClaimGuard, Policy


def test_invalid_evidence_ref_blocks_claim() -> None:
    policy = Policy.load("agentclaimguard/policies/generic_rag.yaml")

    result = AgentClaimGuard(policy).verify(
        claims=[
            {
                "id": "claim_1",
                "type": "citation_required_answer",
                "text": "The refund policy allows cancellation within 14 days.",
                "evidence_refs": ["missing_ev"],
            }
        ],
        evidence=[],
    )

    assert result.status == "blocked"
    assert any(violation.type == "invalid_evidence_ref" for violation in result.violations)

