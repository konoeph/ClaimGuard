# Policy Spec

Policies are YAML files with one top-level `claim_types` mapping.

```yaml
name: strict_policy
version: "0.1"

claim_types:
  numeric_conclusion:
    required_evidence:
      - type: source_fact
        min_count: 2
    required_tool_results:
      - calculator
    forbidden:
      - numeric_claim_without_tool
    fallback:
      verdict: insufficient_evidence
      reason: Numeric conclusions require source facts and calculation results.
```

Supported v0.1 validators:

- `required_evidence`
- `required_tool_results`
- `answer_without_citation`
- `numeric_claim_without_tool`
- `unsupported_pass_fail`
- `use_model_memory_as_authority`

