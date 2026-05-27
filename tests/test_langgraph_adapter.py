from agentclaimguard import Policy
from agentclaimguard.adapters.langgraph import (
    create_evidence_guard_node,
    route_by_guard_status,
)
from agentclaimguard.core.result import ClaimVerificationResult, VerificationResult


def test_langgraph_node_passed() -> None:
    policy = Policy.load_builtin("generic_numeric")
    node = create_evidence_guard_node(policy=policy)

    update = node(
        {
            "claims": [
                {
                    "id": "claim_1",
                    "type": "numeric_conclusion",
                    "text": "Revenue increased by 15%.",
                    "evidence_refs": ["ev_1", "ev_2"],
                    "tool_result_refs": ["tool_1"],
                }
            ],
            "evidence": [
                {"id": "ev_1", "type": "source_fact", "content": "Revenue was 115."},
                {"id": "ev_2", "type": "source_fact", "content": "Revenue was 100."},
            ],
            "tool_results": [
                {
                    "id": "tool_1",
                    "tool_name": "calculator",
                    "status": "success",
                    "output": {"growth_rate": "15%"},
                }
            ],
        }
    )

    assert update["guard_result"].status == "passed"
    assert route_by_guard_status(update) == "passed"


def test_langgraph_node_blocked_missing_tool() -> None:
    policy = Policy.load_builtin("generic_numeric")
    node = create_evidence_guard_node(policy=policy)

    update = node(
        {
            "claims": [
                {
                    "id": "claim_1",
                    "type": "numeric_conclusion",
                    "text": "Revenue increased by 15%.",
                    "evidence_refs": ["ev_1", "ev_2"],
                }
            ],
            "evidence": [
                {"id": "ev_1", "type": "source_fact", "content": "Revenue was 115."},
                {"id": "ev_2", "type": "source_fact", "content": "Revenue was 100."},
            ],
            "tool_results": [],
        }
    )

    result = update["guard_result"]
    assert result.status == "blocked"
    assert result.claim_results[0].status == "tool_required"
    assert route_by_guard_status(update) == "blocked"


def test_langgraph_node_supports_custom_result_key() -> None:
    policy = Policy.load_builtin("generic_numeric")
    node = create_evidence_guard_node(policy=policy, result_key="verification")

    update = node(
        {
            "claims": [
                {
                    "id": "claim_1",
                    "type": "numeric_conclusion",
                    "text": "Revenue increased by 15%.",
                    "evidence_refs": ["ev_1", "ev_2"],
                }
            ],
            "evidence": [
                {"id": "ev_1", "type": "source_fact", "content": "Revenue was 115."},
                {"id": "ev_2", "type": "source_fact", "content": "Revenue was 100."},
            ],
            "tool_results": [],
        }
    )

    assert "verification" in update
    assert route_by_guard_status(update, result_key="verification") == "blocked"


def test_route_by_guard_status() -> None:
    assert route_by_guard_status({}) == "need_check"

    passed = VerificationResult(
        status="passed",
        claim_results=[ClaimVerificationResult(claim_id="claim_1", status="passed")],
    )
    assert route_by_guard_status({"guard_result": passed}) == "passed"

    insufficient_evidence = VerificationResult(
        status="blocked",
        claim_results=[
            ClaimVerificationResult(
                claim_id="claim_1",
                status="insufficient_evidence",
            )
        ],
    )
    assert (
        route_by_guard_status({"guard_result": insufficient_evidence.model_dump()})
        == "insufficient_evidence"
    )

    conflicting_evidence = VerificationResult(
        status="blocked",
        claim_results=[
            ClaimVerificationResult(
                claim_id="claim_1",
                status="conflicting_evidence",
            )
        ],
    )
    assert (
        route_by_guard_status({"guard_result": conflicting_evidence})
        == "conflicting_evidence"
    )
