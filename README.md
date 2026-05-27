# AgentClaimGuard

[![CI](https://github.com/konoeph/AgentClaimGuard/actions/workflows/ci.yml/badge.svg)](https://github.com/konoeph/AgentClaimGuard/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/konoeph/AgentClaimGuard)](https://github.com/konoeph/AgentClaimGuard/releases/latest)
[![License](https://img.shields.io/github/license/konoeph/AgentClaimGuard)](./LICENSE)

AgentClaimGuard is a framework-agnostic evidence gate for LLM agent claims.

It verifies whether important claims in LLM outputs are supported by evidence,
tool results, and user-defined policies.

AgentClaimGuard does not decide whether a claim is true by itself. It verifies
whether a claim is allowed to be returned under a user-defined evidence and tool
policy.

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

## Install

```bash
pip install -e ".[dev,server]"
```

For the LangGraph adapter example:

```bash
pip install -e ".[dev,server,langgraph]"
```

## Quickstart

```bash
pip install -e ".[dev,server]"
python examples/numeric_conclusion/demo.py
uvicorn agentclaimguard.server.main:app --reload
```

```python
from agentclaimguard import AgentClaimGuard, Policy

guard = AgentClaimGuard(Policy.load_builtin("generic_strict"))
result = guard.verify(claims=[], evidence=[], tool_results=[])

print(result.status)
```

## LangGraph Adapter

AgentClaimGuard can run as a LangGraph node between an agent step and routing
logic:

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

Run the minimal adapter demo:

```bash
python examples/langgraph_guard/demo.py
```

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

## What AgentClaimGuard Is Not

AgentClaimGuard is not an agent framework, RAG engine, vector database, or
general-purpose safety guardrail.

It is a claim-level reliability layer for LLM applications.
