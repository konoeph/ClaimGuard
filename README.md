# ClaimGuard

ClaimGuard is a framework-agnostic evidence gate for LLM claims.

It verifies whether important claims in LLM outputs are supported by evidence,
tool results, and user-defined policies.

No evidence, no claim.  
No tool result, no numeric conclusion.  
No source, no compliance judgment.

## Why ClaimGuard?

LLM applications can produce fluent, structured, and confident answers even when
the key claims are unsupported.

RAG gives context, but does not guarantee the answer is grounded. Tool calling
gives results, but does not guarantee the model uses them. Structured output
gives JSON, but does not guarantee the judgment is valid.

ClaimGuard adds a lightweight runtime layer to verify claims before they are
returned to users.

## Install

```bash
pip install -e ".[dev,server]"
```

## Quickstart

```python
from claimguard import ClaimGuard, Policy

policy = Policy.load("claimguard/policies/generic_strict.yaml")
guard = ClaimGuard(policy=policy)

result = guard.verify(
    claims=[
        {
            "id": "claim_1",
            "type": "numeric_conclusion",
            "text": "Revenue increased by 15%.",
            "evidence_refs": ["ev_1", "ev_2"],
            "tool_result_refs": [],
        }
    ],
    evidence=[
        {
            "id": "ev_1",
            "type": "source_fact",
            "source": "annual_report.pdf",
            "locator": "page 12",
            "content": "Revenue in 2025 was 115 million yuan.",
        },
        {
            "id": "ev_2",
            "type": "source_fact",
            "source": "annual_report.pdf",
            "locator": "page 10",
            "content": "Revenue in 2024 was 100 million yuan.",
        },
    ],
    tool_results=[],
)

print(result.status)
print(result.safe_output)
```

The claim is blocked because the policy requires a calculator tool result for
numeric conclusions.

## Core Flow

```text
Claim -> Evidence -> Tool -> Verify
```

## OpenAPI Server

```bash
uvicorn claimguard.server.main:app --reload
```

Then call:

```bash
curl -X POST http://127.0.0.1:8000/v1/verify \
  -H "Content-Type: application/json" \
  -d @examples/numeric_conclusion/sample_input.json
```

## Examples

```bash
python examples/numeric_conclusion/demo.py
python examples/compliance_judgement/demo.py
python examples/rag_citation/demo.py
```

## What ClaimGuard Is Not

ClaimGuard is not an agent framework, RAG engine, vector database, or
general-purpose safety guardrail.

It is a claim-level reliability layer for LLM applications.

