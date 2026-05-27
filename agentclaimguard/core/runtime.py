from collections.abc import Iterable

from agentclaimguard.core.claim import Claim
from agentclaimguard.core.evidence import Evidence
from agentclaimguard.core.policy import Policy
from agentclaimguard.core.result import VerificationResult
from agentclaimguard.core.tool_result import ToolResult
from agentclaimguard.core.verifier import verify_claims as run_verifier


class AgentClaimGuard:
    def __init__(self, policy: Policy):
        self.policy = policy

    def verify(
        self,
        claims: Iterable[Claim | dict],
        evidence: Iterable[Evidence | dict] | None = None,
        tool_results: Iterable[ToolResult | dict] | None = None,
    ) -> VerificationResult:
        parsed_claims = [Claim.model_validate(item) for item in claims]
        parsed_evidence = [Evidence.model_validate(item) for item in evidence or []]
        parsed_tool_results = [
            ToolResult.model_validate(item) for item in tool_results or []
        ]
        return run_verifier(
            claims=parsed_claims,
            evidence=parsed_evidence,
            tool_results=parsed_tool_results,
            policy=self.policy,
        )

    def repair(
        self,
        claims: Iterable[Claim | dict],
        evidence: Iterable[Evidence | dict] | None = None,
        tool_results: Iterable[ToolResult | dict] | None = None,
    ) -> dict:
        result = self.verify(claims=claims, evidence=evidence, tool_results=tool_results)
        return result.safe_output


def verify_claims(
    claims: Iterable[Claim | dict],
    evidence: Iterable[Evidence | dict],
    tool_results: Iterable[ToolResult | dict],
    policy: Policy,
) -> VerificationResult:
    return AgentClaimGuard(policy=policy).verify(
        claims=claims,
        evidence=evidence,
        tool_results=tool_results,
    )

