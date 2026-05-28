# AgentClaimGuard

[![CI](https://github.com/konoeph/AgentClaimGuard/actions/workflows/ci.yml/badge.svg)](https://github.com/konoeph/AgentClaimGuard/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/konoeph/AgentClaimGuard)](https://github.com/konoeph/AgentClaimGuard/releases/latest)
[![License](https://img.shields.io/github/license/konoeph/AgentClaimGuard)](./LICENSE)

Install from PyPI:

```bash
pip install agentclaimguard
```

AgentClaimGuard is a framework-agnostic evidence gate for LLM agent claims.

It verifies whether important claims in LLM outputs are supported by evidence,
tool results, and user-defined policies.

AgentClaimGuard does not decide whether a claim is true by itself. It verifies
whether a claim is allowed to be returned under a user-defined evidence and tool
policy.

AgentClaimGuard is released under Apache-2.0 to support open-source, research,
and commercial integration across LLM agent applications.

No evidence, no claim.  
No tool result, no numeric conclusion.  
No source, no compliance judgment.

## Why AgentClaimGuard?

LLM applications can produce fluent, structured, and confident answers even when
the key claims are unsupported.

RAG gives context, but does not guarantee the answer is grounded. Tool calling
gives results, but does not guarantee the model uses them. Structured output
gives JSON, but does not guarantee the judgment is valid.

AgentClaimGuard adds a lightweight runtime layer to verify claims before they are
returned to users.

## Tiny Example

An agent says:

```text
Revenue increased by 15%.
```

The workflow provides source facts, but no calculator result.

AgentClaimGuard returns:

```text
status=blocked
claim_status=tool_required
safe_verdict=insufficient_evidence
```

The answer can be routed to repair, retrieval, or human review instead of being
returned directly.

## Install

Install from PyPI:

```bash
pip install agentclaimguard
```

With optional adapters and server dependencies:

```bash
pip install "agentclaimguard[server]"
pip install "agentclaimguard[langgraph]"
pip install "agentclaimguard[langchain]"
```

For local development:

```bash
pip install -e ".[dev,server,langgraph,langchain]"
```

## Quickstart

```bash
pip install agentclaimguard
```

```python
from agentclaimguard import AgentClaimGuard, Policy

guard = AgentClaimGuard(Policy.load_builtin("generic_strict"))
result = guard.verify(claims=[], evidence=[], tool_results=[])

print(result.status)
```

To run the FastAPI server:

```bash
pip install "agentclaimguard[server]"
uvicorn agentclaimguard.server.main:app --reload
```

To run the repository demos from a local clone:

```bash
pip install -e ".[dev,server,langgraph,langchain]"
python examples/numeric_conclusion/demo.py
```

## LangGraph Adapter

AgentClaimGuard can run as a LangGraph node between an agent step and routing
logic. Use a typed state schema so LangGraph keeps `guard_result` in the graph
state:

```python
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph
from agentclaimguard import Policy
from agentclaimguard.adapters.langgraph import (
    create_evidence_guard_node,
    route_by_guard_status,
)


class GuardState(TypedDict, total=False):
    claims: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    tool_results: list[dict[str, Any]]
    guard_result: object


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

If your graph uses a different state field, pass the same `result_key` to both
`create_evidence_guard_node(...)` and `route_by_guard_status(...)`.

Run the minimal adapter demo. If `langgraph` is not installed, the demo falls
back to direct node invocation and prints the same guard decision:

```bash
pip install -e ".[langgraph]"
python examples/langgraph_guard/demo.py
```

See [examples/langgraph_guard/README.md](examples/langgraph_guard/README.md) for
the full walkthrough.

## LangChain Adapter

AgentClaimGuard can also wrap a LangChain Runnable and attach verification to
its output:

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
print(result["guard_result"].status)
```

Use `field_map` when the Runnable output uses custom keys for claims, evidence,
or tool results. String-based field maps resolve Runnable output first and then
fall back to Runnable input; callable extractors receive both input and output.
`ainvoke(...)` is also supported for async chains.

By default, the wrapper raises `ValueError` if the Runnable output already
contains the chosen `result_key`. Use a different `result_key`, or set
`overwrite_result=True` when replacement is intentional.

Run the minimal adapter demo:

```bash
python examples/langchain_guard/demo.py
```

## Dify HTTP Tool

AgentClaimGuard can be called from a Dify workflow as a plain HTTP tool using
the FastAPI server:

```text
Dify workflow -> HTTP tool -> POST /v1/verify -> guard decision
```

Run the server and use the example payload:

```bash
pip install "agentclaimguard[server]"
uvicorn agentclaimguard.server.main:app --host 0.0.0.0 --port 8000
curl -X POST http://localhost:8000/v1/verify \
  -H "Content-Type: application/json" \
  --data @examples/dify_http_tool/request.json
```

See [examples/dify_http_tool/README.md](examples/dify_http_tool/README.md) for
the Dify HTTP tool setup notes.

## Claim Extraction Helper

AgentClaimGuard also includes optional deterministic helpers for turning
claim-like items into structured `Claim` objects:

```python
from agentclaimguard.extractors import (
    ClaimExtractionTemplate,
    create_claims_from_items,
)

template = ClaimExtractionTemplate.default()
prompt = template.format(
    answer="Revenue increased by 15%.",
    claim_types=["numeric_conclusion"],
)

extraction = create_claims_from_items([
    {
        "text": "Revenue increased by 15%.",
        "claim_type": "numeric_conclusion",
        "evidence_refs": ["ev_1", "ev_2"],
    }
])
```

The helper does not call an LLM and does not verify truth.

```text
Extraction != Verification
```

See [examples/claim_extraction/README.md](examples/claim_extraction/README.md)
for a minimal extraction-to-verification demo.

## Example Outputs

See [docs/examples.md](docs/examples.md) for full sample output. Short version:

```text
numeric_conclusion  -> blocked / tool_required / insufficient_evidence
compliance_judgement -> blocked / insufficient_evidence / need_check
rag_citation        -> blocked / insufficient_evidence
```

## Core Flow

```text
Claim -> Evidence -> Tool -> Verify
```

## Issues & Roadmap

- Open issues: [GitHub Issues](https://github.com/konoeph/AgentClaimGuard/issues)
- Roadmap: [docs/roadmap.md](docs/roadmap.md)
- Adapter plan: [docs/adapters.md](docs/adapters.md)
- LangChain demo: [examples/langchain_guard/demo.py](examples/langchain_guard/demo.py)
- Claim extraction demo: [examples/claim_extraction/demo.py](examples/claim_extraction/demo.py)
- Dify HTTP tool example: [examples/dify_http_tool/README.md](examples/dify_http_tool/README.md)
- Troubleshooting: [docs/troubleshooting.md](docs/troubleshooting.md)
- Release checklist: [docs/release_checklist.md](docs/release_checklist.md)

## What AgentClaimGuard Is Not

AgentClaimGuard is not an agent framework, RAG engine, vector database, or
general-purpose safety guardrail.

It is a claim-level reliability layer for LLM applications.

## License

Copyright 2026 Hao Peng (彭浩).

AgentClaimGuard is available under the [Apache-2.0 License](LICENSE).
