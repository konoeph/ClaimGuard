# Changelog

All notable changes to AgentClaimGuard will be documented in this file.

## [0.4.0] - 2026-05-28

### Added

- Added optional deterministic claim extraction helpers.
- Added a claim extraction template and extraction-to-verification demo.
- Added tests and documentation for claim extraction warnings, skipped items,
  alias handling, confidence validation, and prompt-only template behavior.

### Changed

- Added a top-level PyPI install note to the README.
- Added a tiny README example showing a blocked numeric claim without a required tool result.

## [0.3.2] - 2026-05-27

### Added

- Added a Dify HTTP tool integration example using the existing FastAPI `/v1/verify` endpoint.

### Changed

- Updated README installation and quickstart commands to use the published PyPI package.

### Maintenance

- Added a manual GitHub Actions workflow for PyPI Trusted Publishing.
- Documented PyPI trusted publisher setup in the release checklist.
- Updated the release checklist to make Trusted Publishing the preferred PyPI path.

## [0.3.1] - 2026-05-27

### Maintenance

- Restored the canonical Apache-2.0 license text for GitHub license detection.
- Added explicit copyright ownership for Hao Peng in project metadata.
- Added package metadata for PyPI project links.
- Added release tooling optional dependencies for build and twine.
- Updated installation and release checklist notes for PyPI readiness.
- Removed duplicate policy-file wheel packaging configuration.

## [0.3.0] - 2026-05-27

### Added

- Added a LangChain Runnable wrapper adapter.
- Added a LangChain adapter demo and tests.
- Added LangChain adapter documentation and quickstart notes.

### Changed

- Clarified LangChain `ainvoke(...)` usage in the demo and docs.
- Made LangChain adapter result-key collisions raise by default unless overwrite is enabled.
- Clarified LangChain field resolution order between Runnable output and input.

### Tests

- Added coverage for LangChain output-first field resolution.
- Added coverage for LangChain input fallback and callable field extractors.
- Added coverage for LangChain non-list field rejection.

### Maintenance

- Updated CI installs to include optional framework adapter dependencies.
- Normalized the Apache-2.0 license text for GitHub license detection.

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
