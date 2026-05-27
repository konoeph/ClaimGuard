from typing import Any, Literal

from pydantic import BaseModel, Field


ClaimStatus = Literal[
    "passed",
    "blocked",
    "need_check",
    "insufficient_evidence",
    "conflicting_evidence",
    "tool_required",
    "tool_error",
    "repair_required",
]


class Violation(BaseModel):
    claim_id: str
    type: str
    message: str
    required: str | None = None
    found: int | None = None
    refs: list[str] = Field(default_factory=list)
    details: dict[str, Any] = Field(default_factory=dict)


class ClaimVerificationResult(BaseModel):
    claim_id: str
    status: ClaimStatus
    violations: list[Violation] = Field(default_factory=list)
    safe_verdict: str | None = None
    reason: str | None = None


class VerificationResult(BaseModel):
    status: Literal["passed", "blocked"]
    claim_results: list[ClaimVerificationResult] = Field(default_factory=list)
    violations: list[Violation] = Field(default_factory=list)
    safe_output: dict[str, Any] = Field(default_factory=dict)

