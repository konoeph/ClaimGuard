from collections.abc import Iterable
from typing import Any

from pydantic import BaseModel, Field, ValidationError, model_validator

from agentclaimguard.core.claim import Claim
from agentclaimguard.utils.ids import new_id


class ClaimCandidate(BaseModel):
    id: str | None = None
    text: str
    type: str = "general"
    verdict: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    tool_result_refs: list[str] = Field(default_factory=list)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def normalize_common_keys(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value

        normalized = dict(value)
        if "claim_id" in normalized and "id" not in normalized:
            normalized["id"] = normalized["claim_id"]
        if "claim_type" in normalized and "type" not in normalized:
            normalized["type"] = normalized["claim_type"]
        return normalized

    def to_claim(self, *, id_prefix: str = "claim") -> Claim:
        return Claim(
            id=self.id or new_id(id_prefix),
            text=self.text.strip(),
            type=self.type,
            verdict=self.verdict,
            evidence_refs=list(self.evidence_refs),
            tool_result_refs=list(self.tool_result_refs),
            confidence=self.confidence,
            metadata=dict(self.metadata),
        )


class ClaimExtractionResult(BaseModel):
    claims: list[Claim] = Field(default_factory=list)
    candidates: list[ClaimCandidate] = Field(default_factory=list)
    skipped_items: list[Any] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


def create_claim_from_text(
    text: str,
    *,
    claim_type: str = "general",
    id: str | None = None,
    verdict: str | None = None,
    evidence_refs: Iterable[str] | None = None,
    tool_result_refs: Iterable[str] | None = None,
    confidence: float | None = None,
    metadata: dict[str, Any] | None = None,
) -> Claim:
    stripped_text = text.strip()
    if not stripped_text:
        raise ValueError("Claim text must not be empty.")

    return Claim(
        id=id or new_id("claim"),
        text=stripped_text,
        type=claim_type,
        verdict=verdict,
        evidence_refs=list(evidence_refs or []),
        tool_result_refs=list(tool_result_refs or []),
        confidence=confidence,
        metadata=dict(metadata or {}),
    )


def create_claims_from_items(
    items: Iterable[str | dict[str, Any] | ClaimCandidate | Claim],
    *,
    default_claim_type: str = "general",
    id_prefix: str = "claim",
) -> ClaimExtractionResult:
    claims: list[Claim] = []
    candidates: list[ClaimCandidate] = []
    skipped_items: list[Any] = []
    warnings: list[str] = []

    for index, item in enumerate(items):
        try:
            candidate = _candidate_from_item(
                item,
                default_claim_type=default_claim_type,
            )
        except (TypeError, ValueError, ValidationError) as exc:
            skipped_items.append(item)
            warnings.append(f"Skipped item {index}: {exc}")
            continue

        claim = candidate.to_claim(id_prefix=id_prefix)
        if not claim.text:
            skipped_items.append(item)
            warnings.append(f"Skipped item {index}: claim text must not be empty.")
            continue

        candidates.append(candidate)
        claims.append(claim)

    return ClaimExtractionResult(
        claims=claims,
        candidates=candidates,
        skipped_items=skipped_items,
        warnings=warnings,
    )


def _candidate_from_item(
    item: str | dict[str, Any] | ClaimCandidate | Claim,
    *,
    default_claim_type: str,
) -> ClaimCandidate:
    if isinstance(item, ClaimCandidate):
        return item

    if isinstance(item, Claim):
        return ClaimCandidate(
            id=item.id,
            text=item.text,
            type=item.type,
            verdict=item.verdict,
            evidence_refs=item.evidence_refs,
            tool_result_refs=item.tool_result_refs,
            confidence=item.confidence,
            metadata=item.metadata,
        )

    if isinstance(item, str):
        stripped_text = item.strip()
        if not stripped_text:
            raise ValueError("Claim text must not be empty.")
        return ClaimCandidate(text=stripped_text, type=default_claim_type)

    if isinstance(item, dict):
        data = dict(item)
        if "type" not in data and "claim_type" not in data:
            data["type"] = default_claim_type
        return ClaimCandidate.model_validate(data)

    raise TypeError(
        "Claim extraction items must be strings, dictionaries, ClaimCandidate, "
        "or Claim objects."
    )
