from typing import Any, Literal

from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    id: str
    tool_name: str
    status: Literal["success", "error", "skipped"] = "success"
    input: dict[str, Any] = Field(default_factory=dict)
    output: Any = None
    evidence_refs: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

