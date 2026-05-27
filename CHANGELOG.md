# Changelog

All notable changes to AgentClaimGuard will be documented in this file.

## [0.1.0] - 2026-05-27

### Added

- Initial AgentClaimGuard core runtime.
- Pydantic schemas for Claim, Evidence, ToolResult, Policy, and VerificationResult.
- YAML-based policy loading.
- Core verifier for claim-level evidence and tool-result checks.
- Basic validators:
  - required evidence check
  - required tool result check
  - citation binding check
  - forbidden verdict check
  - conflicting evidence check
- Built-in generic policies:
  - generic_strict
  - generic_numeric
  - generic_compliance
  - generic_rag
- FastAPI server with:
  - `GET /health`
  - `POST /v1/verify`
  - `POST /v1/repair`
- Example demos:
  - numeric conclusion
  - compliance judgment
  - RAG citation
- Initial documentation and Apache-2.0 license.
- Pytest test suite.

