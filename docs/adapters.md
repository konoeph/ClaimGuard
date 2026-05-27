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
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph
from agentclaimguard import Policy
from agentclaimguard.core.result import VerificationResult
from agentclaimguard.adapters.langgraph import (
    create_evidence_guard_node,
    route_by_guard_status,
)


class GuardState(TypedDict, total=False):
    claims: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    tool_results: list[dict[str, Any]]
    guard_result: VerificationResult
    final_answer: str


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

The top-level `VerificationResult.status` stays `passed` or `blocked`. The
router inspects the first non-passed claim result so graph branches can still
distinguish `insufficient_evidence`, `conflicting_evidence`, and `need_check`.

If your graph uses a different field name, pass the same custom key to both:

```python
guard_node = create_evidence_guard_node(policy=policy, result_key="verification")
route = route_by_guard_status(state, result_key="verification")
```

Run the minimal demo:

```bash
pip install -e ".[dev,server,langgraph]"
python examples/langgraph_guard/demo.py
```

If `langgraph` is not installed, the demo falls back to direct node invocation
so you can still inspect the adapter behavior outside a graph runtime.

## LangChain

The LangChain adapter currently focuses on a Runnable wrapper that runs
AgentClaimGuard after the wrapped Runnable completes.

```python
from langchain_core.runnables import RunnableLambda

from agentclaimguard import Policy
from agentclaimguard.adapters.langchain import create_guarded_runnable

chain = RunnableLambda(lambda payload: {
    "final_answer": payload["question"],
    "claims": payload["claims"],
    "evidence": payload["evidence"],
    "tool_results": payload["tool_results"],
})

guarded = create_guarded_runnable(
    runnable=chain,
    policy=Policy.load_builtin("generic_numeric"),
)

result = guarded.invoke(input_data)
```

The wrapped Runnable should expose structured `claims`, `evidence`, and
`tool_results` in its output or input payload. By default, the adapter looks for
those field names in the Runnable output first, then in the original input.

When your chain uses different keys, provide a `field_map`:

```python
guarded = create_guarded_runnable(
    runnable=chain,
    policy=policy,
    field_map={
        "claims": "structured_claims",
        "evidence": "supporting_evidence",
        "tool_results": "calculator_runs",
    },
    result_key="verification",
)
```

Async chains can use the same wrapper API:

```python
result = await guarded.ainvoke(input_data)
```

If the wrapped Runnable returns a mapping, the adapter appends `guard_result`
under the configured `result_key`. If it returns a non-mapping value, the
adapter wraps it into:

```python
{
    "output": original_output,
    "guard_result": verification_result,
}
```

If the wrapped Runnable already returns the configured `result_key`, the adapter
raises `ValueError` by default. Use `overwrite_result=True` only when that
replacement is intentional.

Run the minimal demo:

```bash
pip install -e ".[dev,server,langchain]"
python examples/langchain_guard/demo.py
```

## Planned Adapters

- LangChain middleware hook
  - Add a deeper integration path after the Runnable wrapper API settles.
- DSPy module wrapper
  - Expose policy-backed assertions as reusable pipeline checks.
- Dify tool plugin
  - Use the verifier as a Tool node or conditional branch.
- RAGFlow post-verifier
  - Convert retrieved context into evidence records, then verify the final answer.

## Design Goal

Adapters should be thin. The core logic stays in the SDK, and each adapter only
translates its host framework into the shared AgentClaimGuard schema.
