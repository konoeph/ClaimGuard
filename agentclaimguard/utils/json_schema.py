from agentclaimguard.core.claim import Claim
from agentclaimguard.core.evidence import Evidence
from agentclaimguard.core.policy import Policy
from agentclaimguard.core.result import VerificationResult
from agentclaimguard.core.tool_result import ToolResult


def export_json_schemas() -> dict:
    return {
        "Claim": Claim.model_json_schema(),
        "Evidence": Evidence.model_json_schema(),
        "ToolResult": ToolResult.model_json_schema(),
        "Policy": Policy.model_json_schema(),
        "VerificationResult": VerificationResult.model_json_schema(),
    }

