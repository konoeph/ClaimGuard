# Changelog

All notable changes to AgentClaimGuard will be documented in this file.

## [Unreleased]

### Added

- Added a LangChain Runnable wrapper adapter.
- Added a LangChain adapter demo and tests.
- Added LangChain adapter documentation and quickstart notes.

## [0.2.1] - 2026-05-27

### Added

- Added a pull request template for release-oriented validation.
- Added clearer LangGraph demo notes under `examples/langgraph_guard/`.
- Added troubleshooting notes for common LangGraph adapter issues.
- Added a release checklist for maintainers.

### Changed

- Clarified README and adapter docs around LangGraph typed state usage.
- Clarified custom `result_key` usage for the LangGraph adapter helpers.
- Improved issue templates for integration-specific bug reports and feature requests.

### Maintenance

- Updated GitHub Actions workflow dependencies to Node 24 compatible versions.

## [0.2.0] - 2026-05-27

### Added

- LangGraph evidence guard node adapter.
- Guard status routing helper for LangGraph conditional edges.
- Built-in policy loader helper.
- Minimal LangGraph adapter demo.
- Adapter tests for passed, blocked, and routed guard results.

## [0.1.1] - 2026-05-27

### Added

- README badges.
- Example output documentation.
- Roadmap documentation.
- Adapter planning documentation.
- GitHub issue templates.

### Changed

- Improved README quickstart and project positioning.

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
