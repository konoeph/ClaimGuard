# LangGraph Guard Example

This example shows how AgentClaimGuard can sit between an agent node and route
logic in a LangGraph workflow.

## What it demonstrates

- an agent produces a `numeric_conclusion` claim
- the claim has source facts but no calculator tool result
- `create_evidence_guard_node(...)` verifies the state
- `route_by_guard_status(...)` sends the flow to a repair step

## Install

```bash
pip install -e ".[dev,server,langgraph]"
```

## Run

```bash
python examples/langgraph_guard/demo.py
```

If `langgraph` is not installed, the script falls back to direct node
invocation and still prints the same guard outcome.

## Expected output

```text
guard_status=blocked
claim_status=tool_required
route=blocked
final_answer=Need calculator result before returning numeric conclusion.
```

## State shape

The example keeps the graph state intentionally small:

```python
{
    "claims": [...],
    "evidence": [...],
    "tool_results": [...],
    "guard_result": ...,
    "final_answer": "...",
}
```

Use a typed state schema with LangGraph so `guard_result` remains available to
later nodes and route logic.
