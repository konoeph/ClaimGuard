# LangChain Guard Example

This example shows how AgentClaimGuard can wrap a LangChain Runnable and attach
verification results to the Runnable output.

## What it demonstrates

- a Runnable returns structured `claims`, `evidence`, and `tool_results`
- `create_guarded_runnable(...)` runs AgentClaimGuard after the Runnable
- the original output is returned with `guard_result` attached
- a numeric claim without a calculator result is blocked
- both `invoke(...)` and `ainvoke(...)` paths

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
sync_final_answer=Revenue increased by 15%.
sync_guard_status=blocked
sync_claim_status=tool_required
async_final_answer=Revenue increased by 15%.
async_guard_status=blocked
async_claim_status=tool_required
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

## Field resolution

- Put `claims`, `evidence`, and `tool_results` in the input when they are
  prepared before the chain runs.
- Return them in the output when the Runnable itself produces or transforms
  them.
- Output fields take precedence over input fields for string-based `field_map`
  entries.
- Callable field extractors receive both `input` and `output` and can choose
  either source directly.

## Result key collisions

If the wrapped Runnable already returns a `guard_result` field, the adapter
raises `ValueError` by default instead of silently overwriting it.

Use either:

- a different `result_key`, or
- `overwrite_result=True` if replacement is intentional
