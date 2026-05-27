# Adapters

AgentClaimGuard adapters keep the core verifier framework-agnostic while making
it easier to embed claim checks inside existing LLM application workflows.

## Runtime Contract

Every adapter follows the same core runtime contract:

```text
claims + evidence + tool_results + policy -> verify -> status + violations + safe fallback
```

## LangGraph

The LangGraph adapter exposes a verification node and a routing helper:

```python
from langgraph.graph import END, StateGraph
from agentclaimguard import Policy
from agentclaimguard.adapters.langgraph import (
    create_evidence_guard_node,
    route_by_guard_status,
)

policy = Policy.load_builtin("generic_numeric")
guard_node = create_evidence_guard_node(policy=policy)

builder = StateGraph(dict)
builder.add_node("agent", agent_node)
builder.add_node("guard", guard_node)
builder.add_node("repair", repair_node)
builder.add_node("human_review", human_review_node)

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
```

The default state shape is intentionally plain:

```python
{
    "claims": [...],
    "evidence": [...],
    "tool_results": [...],
    "guard_result": None,
    "final_answer": "...",
}
```

`create_evidence_guard_node(...)` reads `claims`, `evidence`, and
`tool_results`, then returns a state update containing `guard_result`.
`route_by_guard_status(...)` maps the guard result to one of:

```text
passed
blocked
need_check
insufficient_evidence
conflicting_evidence
```

Run the minimal demo:

```bash
pip install -e ".[langgraph]"
python examples/langgraph_guard/demo.py
```

## Planned Adapters

- LangChain middleware or Runnable wrapper
  - Wrap the verifier after output parsing.
  - Use it as a post-check or repair step in an existing chain.
- DSPy module wrapper
  - Expose policy-backed assertions as reusable pipeline checks.
- Dify tool plugin
  - Use the verifier as a Tool node or conditional branch.
- RAGFlow post-verifier
  - Convert retrieved context into evidence records, then verify the final answer.

## Design Goal

Adapters should be thin. The core logic stays in the SDK, and each adapter only
translates its host framework into the shared AgentClaimGuard schema.
