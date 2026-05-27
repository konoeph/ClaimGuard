from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, model_validator

from claimguard.utils.yaml_loader import load_yaml


class EvidenceRequirement(BaseModel):
    type: str
    min_count: int = Field(default=1, ge=1)


class ToolRequirement(BaseModel):
    tool_name: str
    min_count: int = Field(default=1, ge=1)

    @model_validator(mode="before")
    @classmethod
    def parse_string_requirement(cls, value: Any) -> Any:
        if isinstance(value, str):
            return {"tool_name": value}
        if isinstance(value, dict) and "name" in value and "tool_name" not in value:
            return {**value, "tool_name": value["name"]}
        return value


class FallbackRule(BaseModel):
    verdict: str = "need_check"
    reason: str | None = None


class ClaimTypePolicy(BaseModel):
    required_evidence: list[EvidenceRequirement] = Field(default_factory=list)
    required_tool_results: list[ToolRequirement] = Field(default_factory=list)
    forbidden: list[str] = Field(default_factory=list)
    fallback: FallbackRule | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Policy(BaseModel):
    name: str = "default"
    version: str = "0.1"
    claim_types: dict[str, ClaimTypePolicy] = Field(default_factory=dict)
    default_fallback: FallbackRule = Field(
        default_factory=lambda: FallbackRule(
            verdict="need_check",
            reason="The claim could not be verified by the active policy.",
        )
    )
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def load(cls, path: str | Path) -> "Policy":
        data = load_yaml(path)
        return cls.model_validate(data)

    def policy_for_claim_type(self, claim_type: str) -> ClaimTypePolicy:
        return self.claim_types.get(claim_type, ClaimTypePolicy())

    def fallback_for_claim_type(self, claim_type: str) -> FallbackRule:
        claim_policy = self.policy_for_claim_type(claim_type)
        return claim_policy.fallback or self.default_fallback

