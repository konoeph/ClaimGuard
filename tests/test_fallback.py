from agentclaimguard import AgentClaimGuard, Policy


def test_fallback_verdict_is_returned_for_failed_claim() -> None:
    policy = Policy.load("agentclaimguard/policies/generic_compliance.yaml")

    result = AgentClaimGuard(policy).verify(
        claims=[
            {
                "id": "claim_1",
                "type": "compliance_judgement",
                "text": "This practice is compliant.",
                "verdict": "pass",
                "evidence_refs": [],
            }
        ]
    )

    assert result.status == "blocked"
    assert result.claim_results[0].safe_verdict == "need_check"
    assert result.safe_output["blocked_claims"][0]["safe_verdict"] == "need_check"

