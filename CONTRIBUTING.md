# Contributing

Thanks for your interest in AgentClaimGuard.

AgentClaimGuard is intentionally small in v0.1. The project focuses on one boundary:
structured claims come in, and AgentClaimGuard checks whether those claims are allowed
to be returned under a user-defined evidence and tool policy.

## Development Setup

```bash
pip install -e ".[dev,server]"
```

## Verify Changes

```bash
python -m pytest -q
python -m compileall agentclaimguard examples tests
```

## Contribution Guidelines

- Keep v0.1 changes focused on the core runtime, schemas, policies, examples,
  documentation, and tests.
- Prefer explicit, deterministic policy checks before adding semantic or
  LLM-based verification.
- Do not add framework adapters, claim extraction, UI, or industry-specific
  policy packs without first discussing the scope.
- Add tests for behavior changes.
- Keep public APIs small and easy to explain.

## Commit Style

Use short conventional-style commit messages when possible:

```text
feat: add policy validator
fix: handle missing tool result refs
docs: clarify evidence model
chore: update CI
```

