from typing import Any

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    id: str
    type: str
    source: str | None = None
    locator: str | None = None
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)

