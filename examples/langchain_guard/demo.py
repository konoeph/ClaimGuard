from langchain_core.runnables import RunnableLambda

from agentclaimguard import Policy
from agentclaimguard.adapters.langchain import create_guarded_runnable


def main() -> None:
    policy = Policy.load_builtin("generic_numeric")

    chain = RunnableLambda(
        lambda payload: {
            "final_answer": payload["question"],
            "claims": payload["claims"],
            "evidence": payload["evidence"],
            "tool_results": payload["tool_results"],
        }
    )

    guarded = create_guarded_runnable(runnable=chain, policy=policy)
    result = guarded.invoke(
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
                {"id": "ev_1", "type": "source_fact", "content": "Revenue was 115."},
                {"id": "ev_2", "type": "source_fact", "content": "Revenue was 100."},
            ],
            "tool_results": [],
        }
    )

    print(f"final_answer={result['final_answer']}")
    print(f"guard_status={result['guard_result'].status}")
    print(f"claim_status={result['guard_result'].claim_results[0].status}")


if __name__ == "__main__":
    main()
