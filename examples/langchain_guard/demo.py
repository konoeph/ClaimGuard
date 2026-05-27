import asyncio

from langchain_core.runnables import RunnableLambda

from agentclaimguard import Policy
from agentclaimguard.adapters.langchain import create_guarded_runnable


def build_guarded_runnable():
    policy = Policy.load_builtin("generic_numeric")

    chain = RunnableLambda(
        lambda payload: {
            "final_answer": payload["question"],
            "claims": payload["claims"],
            "evidence": payload["evidence"],
            "tool_results": payload["tool_results"],
        }
    )

    return create_guarded_runnable(runnable=chain, policy=policy)


def build_input() -> dict:
    return {
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
            {"id": "ev_1", "type": "source_fact", "content": "Revenue was 115."},
            {"id": "ev_2", "type": "source_fact", "content": "Revenue was 100."},
        ],
        "tool_results": [],
    }


def print_result(result: dict, *, prefix: str) -> None:
    print(f"{prefix}_final_answer={result['final_answer']}")
    print(f"{prefix}_guard_status={result['guard_result'].status}")
    print(f"{prefix}_claim_status={result['guard_result'].claim_results[0].status}")


def main() -> None:
    guarded = build_guarded_runnable()
    result = guarded.invoke(build_input())
    print_result(result, prefix="sync")

    async_result = asyncio.run(guarded.ainvoke(build_input()))
    print_result(async_result, prefix="async")


if __name__ == "__main__":
    main()
