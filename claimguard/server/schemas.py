from pydantic import BaseModel, Field

from claimguard.core.claim import Claim
from claimguard.core.evidence import Evidence
from claimguard.core.policy import Policy
from claimguard.core.tool_result import ToolResult


class VerifyRequest(BaseModel):
    claims: list[Claim]
    evidence: list[Evidence] = Field(default_factory=list)
    tool_results: list[ToolResult] = Field(default_factory=list)
    policy: Policy | None = None


class RepairRequest(VerifyRequest):
    pass

