import asyncio

from langchain_core.runnables import RunnableLambda

from agentclaimguard import Policy
from agentclaimguard.adapters.langchain import create_guarded_runnable


def test_guarded_runnable_attaches_guard_result_to_mapping_output() -> None:
    policy = Policy.load_builtin("generic_numeric")
    runnable = RunnableLambda(
        lambda payload: {
            "final_answer": payload["question"],
            "claims": payload["claims"],
            "evidence": payload["evidence"],
            "tool_results": payload["tool_results"],
        }
    )

    guarded = create_guarded_runnable(runnable=runnable, policy=policy)
    result = guarded.invoke(
        {
            "question": "Revenue increased by 15%.",
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

    assert result["final_answer"] == "Revenue increased by 15%."
    assert result["guard_result"].status == "passed"


def test_guarded_runnable_supports_custom_field_map_and_result_key() -> None:
    policy = Policy.load_builtin("generic_numeric")
    runnable = RunnableLambda(
        lambda payload: {
            "answer": payload["question"],
            "structured_claims": payload["agent_claims"],
            "supporting_evidence": payload["supporting_evidence"],
            "calculator_runs": payload["calculator_runs"],
        }
    )

    guarded = create_guarded_runnable(
        runnable=runnable,
        policy=policy,
        field_map={
            "claims": "structured_claims",
            "evidence": "supporting_evidence",
            "tool_results": "calculator_runs",
        },
        result_key="verification",
    )

    result = guarded.invoke(
        {
            "question": "Revenue increased by 15%.",
            "agent_claims": [
                {
                    "id": "claim_1",
                    "type": "numeric_conclusion",
                    "text": "Revenue increased by 15%.",
                    "evidence_refs": ["ev_1", "ev_2"],
                }
            ],
            "supporting_evidence": [
                {"id": "ev_1", "type": "source_fact", "content": "Revenue was 115."},
                {"id": "ev_2", "type": "source_fact", "content": "Revenue was 100."},
            ],
            "calculator_runs": [],
        }
    )

    assert result["answer"] == "Revenue increased by 15%."
    assert result["verification"].status == "blocked"
    assert result["verification"].claim_results[0].status == "tool_required"


def test_guarded_runnable_wraps_non_mapping_output() -> None:
    policy = Policy.load_builtin("generic_numeric")
    runnable = RunnableLambda(
        lambda payload: payload["claims"]
    )

    guarded = create_guarded_runnable(
        runnable=runnable,
        policy=policy,
        output_key="claims_output",
    )

    result = guarded.invoke(
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

    assert "claims_output" in result
    assert result["guard_result"].status == "blocked"


def test_guarded_runnable_ainvoke_blocks_missing_tool_result() -> None:
    policy = Policy.load_builtin("generic_numeric")
    runnable = RunnableLambda(
        lambda payload: {
            "final_answer": payload["question"],
            "claims": payload["claims"],
            "evidence": payload["evidence"],
            "tool_results": payload["tool_results"],
        }
    )

    guarded = create_guarded_runnable(runnable=runnable, policy=policy)
    result = asyncio.run(
        guarded.ainvoke(
            {
                "question": "Revenue increased by 15%.",
                "claims": [
                    {
                        "id": "claim_1",
                        "type": "numeric_conclusion",
                        "text": "Revenue increased by 15%.",
                        "evidence_refs": ["ev_1", "ev_2"],
                    }
                ],
                "evidence": [
                    {
                        "id": "ev_1",
                        "type": "source_fact",
                        "content": "Revenue was 115.",
                    },
                    {
                        "id": "ev_2",
                        "type": "source_fact",
                        "content": "Revenue was 100.",
                    },
                ],
                "tool_results": [],
            }
        )
    )

    assert result["guard_result"].status == "blocked"
    assert result["guard_result"].claim_results[0].status == "tool_required"


def test_guarded_runnable_raises_on_result_key_collision_by_default() -> None:
    policy = Policy.load_builtin("generic_numeric")
    runnable = RunnableLambda(
        lambda payload: {
            "guard_result": "existing value",
            "claims": payload["claims"],
            "evidence": payload["evidence"],
            "tool_results": payload["tool_results"],
        }
    )
    guarded = create_guarded_runnable(runnable=runnable, policy=policy)

    try:
        guarded.invoke(
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
    except ValueError as exc:
        assert "already contains 'guard_result'" in str(exc)
    else:
        raise AssertionError("Expected ValueError for result_key collision.")


def test_guarded_runnable_can_overwrite_result_key_when_enabled() -> None:
    policy = Policy.load_builtin("generic_numeric")
    runnable = RunnableLambda(
        lambda payload: {
            "guard_result": "existing value",
            "claims": payload["claims"],
            "evidence": payload["evidence"],
            "tool_results": payload["tool_results"],
        }
    )
    guarded = create_guarded_runnable(
        runnable=runnable,
        policy=policy,
        overwrite_result=True,
    )

    result = guarded.invoke(
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

    assert result["guard_result"].status == "blocked"
