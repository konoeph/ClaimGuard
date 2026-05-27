from typing import Any

from pydantic import BaseModel, Field


class Claim(BaseModel):
    id: str
    text: str
    type: str
    verdict: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    tool_result_refs: list[str] = Field(default_factory=list)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)

