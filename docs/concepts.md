# Concepts

AgentClaimGuard verifies claim-level reliability with a simple flow:

```text
Claim -> Evidence -> Tool -> Verify
```

## Claim

A claim is a key conclusion, assertion, judgment, or recommendation produced by
an LLM application.

## Evidence

Evidence is source material that can support a claim, such as retrieved context,
database records, regulations, table cells, API responses, or user input.

## Tool Result

Tool results are outputs from calculators, SQL queries, linters, tests, unit
converters, or other deterministic systems.

## Policy

A policy defines which evidence and tool results are required for each claim
type, plus the fallback verdict to use when verification fails.

