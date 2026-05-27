from pydantic import BaseModel, Field

from agentclaimguard.core.claim import Claim
from agentclaimguard.core.evidence import Evidence
from agentclaimguard.core.policy import Policy
from agentclaimguard.core.tool_result import ToolResult


class VerifyRequest(BaseModel):
    claims: list[Claim]
    evidence: list[Evidence] = Field(default_factory=list)
    tool_results: list[ToolResult] = Field(default_factory=list)
    policy: Policy | None = None


class RepairRequest(VerifyRequest):
    pass

