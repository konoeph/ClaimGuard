# Schema Spec

The public schemas are Pydantic models:

- `Claim`
- `Evidence`
- `ToolResult`
- `Policy`
- `VerificationResult`

Export JSON schemas with:

```python
from agentclaimguard.utils.json_schema import export_json_schemas

schemas = export_json_schemas()
```

