# Example Outputs

These are the expected high-level outcomes from the bundled demos.

## Numeric Conclusion

```text
$ python examples/numeric_conclusion/demo.py
{
  "status": "blocked",
  "claim_results": [
    {
      "claim_id": "claim_1",
      "status": "tool_required",
      "safe_verdict": "insufficient_evidence"
    }
  ]
}
```

## Compliance Judgment

```text
$ python examples/compliance_judgement/demo.py
{
  "status": "blocked",
  "claim_results": [
    {
      "claim_id": "claim_2",
      "status": "insufficient_evidence",
      "safe_verdict": "need_check"
    }
  ]
}
```

## RAG Citation

```text
$ python examples/rag_citation/demo.py
{
  "status": "blocked",
  "claim_results": [
    {
      "claim_id": "claim_3",
      "status": "insufficient_evidence",
      "safe_verdict": "insufficient_evidence"
    }
  ]
}
```

