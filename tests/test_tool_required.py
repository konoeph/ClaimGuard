from agentclaimguard import AgentClaimGuard, Policy


def test_missing_required_tool_blocks_numeric_claim() -> None:
    policy = Policy.load("agentclaimguard/policies/generic_numeric.yaml")

    result = AgentClaimGuard(policy).verify(
        claims=[
            {
                "id": "claim_1",
                "type": "numeric_conclusion",
                "text": "Revenue increased by 15%.",
                "evidence_refs": ["ev_1", "ev_2"],
            }
        ],
        evidence=[
            {"id": "ev_1", "type": "source_fact", "content": "Revenue was 115."},
            {"id": "ev_2", "type": "source_fact", "content": "Revenue was 100."},
        ],
    )

    assert result.status == "blocked"
    assert result.claim_results[0].status == "tool_required"
    assert any(
        violation.type == "missing_required_tool_result"
        for violation in result.violations
    )


def test_successful_required_tool_passes_numeric_claim() -> None:
    policy = Policy.load("agentclaimguard/policies/generic_numeric.yaml")

    result = AgentClaimGuard(policy).verify(
        claims=[
            {
                "id": "claim_1",
                "type": "numeric_conclusion",
                "text": "Revenue increased by 15%.",
                "evidence_refs": ["ev_1", "ev_2"],
                "tool_result_refs": ["tool_1"],
            }
        ],
        evidence=[
            {"id": "ev_1", "type": "source_fact", "content": "Revenue was 115."},
            {"id": "ev_2", "type": "source_fact", "content": "Revenue was 100."},
        ],
        tool_results=[
            {
                "id": "tool_1",
                "tool_name": "calculator",
                "status": "success",
                "output": {"growth_rate": "15%"},
            }
        ],
    )

    assert result.status == "passed"
    assert result.violations == []

