from typing import Any, TypedDict

from agentclaimguard import Policy
from agentclaimguard.adapters.langgraph import (
    create_evidence_guard_node,
    route_by_guard_status,
)
from agentclaimguard.core.result import VerificationResult


class GuardState(TypedDict, total=False):
    claims: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    tool_results: list[dict[str, Any]]
    guard_result: VerificationResult
    final_answer: str


def agent_node(state: GuardState) -> GuardState:
    return {
        **state,
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
        "final_answer": "Revenue increased by 15%.",
    }


def repair_node(state: GuardState) -> GuardState:
    return {"final_answer": "Need calculator result before returning numeric conclusion."}


def human_review_node(state: GuardState) -> GuardState:
    return {"final_answer": "Needs human review before release."}


def run_without_langgraph() -> None:
    policy = Policy.load_builtin("generic_numeric")
    guard_node = create_evidence_guard_node(policy=policy)

    state = agent_node({})
    state.update(guard_node(state))
    route = route_by_guard_status(state)

    if route == "blocked":
        state = repair_node(state)
    elif route in {"need_check", "insufficient_evidence", "conflicting_evidence"}:
        state = human_review_node(state)

    result = state["guard_result"]
    print(f"guard_status={result.status}")
    print(f"claim_status={result.claim_results[0].status}")
    print(f"route={route}")
    print(f"final_answer={state['final_answer']}")


def run_with_langgraph() -> None:
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError:
        run_without_langgraph()
        return

    policy = Policy.load_builtin("generic_numeric")
    guard_node = create_evidence_guard_node(policy=policy)

    builder = StateGraph(GuardState)
    builder.add_node("agent", agent_node)
    builder.add_node("guard", guard_node)
    builder.add_node("repair", repair_node)
    builder.add_node("human_review", human_review_node)

    builder.add_edge(START, "agent")
    builder.add_edge("agent", "guard")
    builder.add_conditional_edges(
        "guard",
        route_by_guard_status,
        {
            "passed": END,
            "blocked": "repair",
            "need_check": "human_review",
            "insufficient_evidence": "human_review",
            "conflicting_evidence": "human_review",
        },
    )
    builder.add_edge("repair", END)
    builder.add_edge("human_review", END)

    state = builder.compile().invoke({})
    route = route_by_guard_status(state)
    result = state["guard_result"]

    print(f"guard_status={result.status}")
    print(f"claim_status={result.claim_results[0].status}")
    print(f"route={route}")
    print(f"final_answer={state['final_answer']}")


if __name__ == "__main__":
    run_with_langgraph()
