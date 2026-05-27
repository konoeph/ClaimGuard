# Troubleshooting

## LangGraph `guard_result` Is Missing

Use a typed LangGraph state schema and include `guard_result` in the state
definition.

Example:

```python
from typing import Any, TypedDict

from agentclaimguard.core.result import VerificationResult


class GuardState(TypedDict, total=False):
    claims: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    tool_results: list[dict[str, Any]]
    guard_result: VerificationResult
    final_answer: str
```

If you use `StateGraph(dict)` without a typed state, graph updates may not keep
the verification result in later nodes.

## `route_by_guard_status(...)` Always Returns `need_check`

Make sure the guard node and router use the same `result_key`.

Example:

```python
guard_node = create_evidence_guard_node(
    policy=policy,
    result_key="verification",
)

route = route_by_guard_status(state, result_key="verification")
```

If the node writes to `verification` but the router still reads `guard_result`,
the router will behave as if no result is present.

## The Demo Runs Without LangGraph Installed

`examples/langgraph_guard/demo.py` prefers a real LangGraph run when
`langgraph` is installed.

If it is not installed, the script falls back to direct node invocation so you
can still inspect the guard decision and expected routing outcome.

Install the optional dependency to run the full graph example:

```bash
pip install -e ".[dev,server,langgraph]"
```

## My Claim Is Blocked Unexpectedly

Check these inputs first:

- claim type
- active policy
- required evidence
- required tool results
- `evidence_refs`
- `tool_result_refs`

For numeric claims in the bundled policies, the most common cause is a missing
calculator tool result or missing source facts.

## The Top-Level Result Only Shows `blocked`

This is expected.

`VerificationResult.status` stays at a coarse `passed` or `blocked` level.
Adapter routing helpers inspect the first non-passed claim result to surface
more specific outcomes such as:

- `insufficient_evidence`
- `conflicting_evidence`
- `need_check`
- `blocked`
