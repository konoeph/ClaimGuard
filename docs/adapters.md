# Adapters

The current release focuses on the framework-agnostic SDK and OpenAPI server.

## Near-Term Shapes

Planned integration points follow the same core runtime contract:

```text
claims + evidence + tool_results + policy -> verify -> status + violations + safe fallback
```

## Planned Adapters

- LangChain middleware or Runnable wrapper
  - Wrap the verifier after output parsing.
  - Use it as a post-check or repair step in an existing chain.
- LangGraph node
  - Place it between the agent node and the route logic.
  - Let the node decide whether to continue, repair, or stop.
- DSPy module wrapper
  - Expose policy-backed assertions as reusable pipeline checks.
- Dify tool plugin
  - Use the verifier as a Tool node or conditional branch.
- RAGFlow post-verifier
  - Convert retrieved context into evidence records, then verify the final answer.

## Design Goal

Adapters should be thin. The core logic stays in the SDK, and each adapter only
translates its host framework into the shared ClaimGuard schema.
