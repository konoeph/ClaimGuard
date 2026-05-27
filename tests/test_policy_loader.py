from pathlib import Path

from agentclaimguard import Policy


def test_policy_loader_loads_generic_policy() -> None:
    policy = Policy.load(Path("agentclaimguard/policies/generic_strict.yaml"))

    assert policy.name == "generic_strict"
    assert "numeric_conclusion" in policy.claim_types
    numeric_policy = policy.claim_types["numeric_conclusion"]
    assert numeric_policy.required_evidence[0].type == "source_fact"
    assert numeric_policy.required_tool_results[0].tool_name == "calculator"


def test_policy_loader_loads_builtin_policy() -> None:
    policy = Policy.load_builtin("generic_numeric")

    assert policy.name == "generic_numeric"
    assert "numeric_conclusion" in policy.claim_types
