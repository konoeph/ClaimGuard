# LangChain Guard Example

This example shows how AgentClaimGuard can wrap a LangChain Runnable and attach
verification results to the Runnable output.

## What it demonstrates

- a Runnable returns structured `claims`, `evidence`, and `tool_results`
- `create_guarded_runnable(...)` runs AgentClaimGuard after the Runnable
- the original output is returned with `guard_result` attached
- a numeric claim without a calculator result is blocked

## Install

```bash
pip install -e ".[dev,server,langchain]"
```

## Run

```bash
python examples/langchain_guard/demo.py
```

## Expected output

```text
final_answer=Revenue increased by 15%.
guard_status=blocked
claim_status=tool_required
```

## Custom field mapping

If your Runnable uses different keys, pass a `field_map`:

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
