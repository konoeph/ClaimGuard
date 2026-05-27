# Dify HTTP Tool Example

This example shows how to call AgentClaimGuard from a Dify workflow as a plain
HTTP tool.

It does not require a Dify plugin package. The flow uses the existing
AgentClaimGuard FastAPI server:

```text
Dify workflow -> HTTP tool -> POST /v1/verify -> guard decision
```

## What It Demonstrates

- a workflow prepares structured `claims`, `evidence`, and `tool_results`
- Dify calls AgentClaimGuard as an HTTP tool
- AgentClaimGuard blocks a numeric claim that lacks a calculator result
- the workflow can route `blocked` results to repair or human review

## Start AgentClaimGuard

Install the server extra and start the API locally:

```bash
pip install "agentclaimguard[server]"
uvicorn agentclaimguard.server.main:app --host 0.0.0.0 --port 8000
```

For local repository development:

```bash
pip install -e ".[dev,server]"
uvicorn agentclaimguard.server.main:app --host 0.0.0.0 --port 8000
```

## Configure A Dify HTTP Tool

Use these HTTP settings:

```text
Method: POST
URL: http://<agentclaimguard-host>:8000/v1/verify
Headers:
  Content-Type: application/json
Body:
  JSON object with claims, evidence, and tool_results
```

Use `request.json` as the body template.

## Try With curl

From this repository:

```bash
curl -X POST http://localhost:8000/v1/verify \
  -H "Content-Type: application/json" \
  --data @examples/dify_http_tool/request.json
```

Expected high-level result:

```text
status=blocked
claim_status=tool_required
safe_verdict=insufficient_evidence
```

See `response_blocked.json` for a representative response.

## Dify Routing Pattern

In a Dify workflow, route by the returned `status`:

```text
passed  -> return answer
blocked -> repair, retrieve more evidence, or human review
```

For individual claim handling, inspect `claim_results[0].status` and
`claim_results[0].safe_verdict`.

## Boundary

AgentClaimGuard does not extract claims from free text in this example. The Dify
workflow is responsible for preparing structured claims, evidence, and tool
results before calling `/v1/verify`.
