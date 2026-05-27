from claimguard.core.claim import Claim
from claimguard.core.policy import ClaimTypePolicy
from claimguard.core.result import Violation
from claimguard.core.tool_result import ToolResult


def validate_required_tools(
    claim: Claim,
    tool_results_by_id: dict[str, ToolResult],
    claim_policy: ClaimTypePolicy,
) -> list[Violation]:
    violations: list[Violation] = []
    referenced_tools = [
        tool_results_by_id[ref]
        for ref in claim.tool_result_refs
        if ref in tool_results_by_id
    ]

    for requirement in claim_policy.required_tool_results:
        matching_tools = [
            tool
            for tool in referenced_tools
            if tool.tool_name == requirement.tool_name
        ]
        successful_count = sum(1 for tool in matching_tools if tool.status == "success")

        if matching_tools and successful_count < requirement.min_count:
            violations.append(
                Violation(
                    claim_id=claim.id,
                    type="required_tool_error",
                    message=(
                        f"Claim references '{requirement.tool_name}', but the "
                        "required successful tool result is unavailable."
                    ),
                    required=requirement.tool_name,
                    found=successful_count,
                    refs=[tool.id for tool in matching_tools],
                )
            )
            continue

        if successful_count < requirement.min_count:
            violations.append(
                Violation(
                    claim_id=claim.id,
                    type="missing_required_tool_result",
                    message=(
                        f"Claim requires at least {requirement.min_count} "
                        f"successful '{requirement.tool_name}' tool result(s)."
                    ),
                    required=requirement.tool_name,
                    found=successful_count,
                    refs=claim.tool_result_refs,
                )
            )

    return violations

