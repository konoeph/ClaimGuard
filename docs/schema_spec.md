# Schema Spec

The public schemas are Pydantic models:

- `Claim`
- `Evidence`
- `ToolResult`
- `Policy`
- `VerificationResult`

Export JSON schemas with:

```python
from claimguard.utils.json_schema import export_json_schemas

schemas = export_json_schemas()
```

