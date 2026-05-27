from claimguard.core.claim import Claim
from claimguard.core.evidence import Evidence
from claimguard.core.policy import Policy
from claimguard.core.result import VerificationResult
from claimguard.core.tool_result import ToolResult


def export_json_schemas() -> dict:
    return {
        "Claim": Claim.model_json_schema(),
        "Evidence": Evidence.model_json_schema(),
        "ToolResult": ToolResult.model_json_schema(),
        "Policy": Policy.model_json_schema(),
        "VerificationResult": VerificationResult.model_json_schema(),
    }

