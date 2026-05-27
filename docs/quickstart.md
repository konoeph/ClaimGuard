# Quickstart

Install ClaimGuard in editable mode while developing:

```bash
pip install -e ".[dev,server]"
```

Run a demo:

```bash
python examples/numeric_conclusion/demo.py
```

Start the OpenAPI server:

```bash
uvicorn claimguard.server.main:app --reload
```

Submit a verification request:

```bash
curl -X POST http://127.0.0.1:8000/v1/verify \
  -H "Content-Type: application/json" \
  -d @examples/numeric_conclusion/sample_input.json
```

