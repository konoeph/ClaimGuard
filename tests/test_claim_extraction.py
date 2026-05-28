from agentclaimguard import AgentClaimGuard, Claim, Policy
from agentclaimguard.extractors import (
    ClaimCandidate,
    ClaimExtractionTemplate,
    create_claim_from_text,
    create_claims_from_items,
)


def test_create_claim_from_text_builds_claim() -> None:
    claim = create_claim_from_text(
        "Revenue increased by 15%.",
        claim_type="numeric_conclusion",
        id="claim_1",
        evidence_refs=["ev_1", "ev_2"],
        tool_result_refs=["tool_1"],
        confidence=0.9,
        metadata={"source": "unit_test"},
    )

    assert isinstance(claim, Claim)
    assert claim.id == "claim_1"
    assert claim.type == "numeric_conclusion"
    assert claim.evidence_refs == ["ev_1", "ev_2"]
    assert claim.tool_result_refs == ["tool_1"]
    assert claim.confidence == 0.9
    assert claim.metadata == {"source": "unit_test"}


def test_create_claims_from_items_supports_string_dict_and_candidate() -> None:
    result = create_claims_from_items(
        [
            "Revenue increased by 15%.",
            {
                "claim_id": "claim_2",
                "claim_type": "numeric_conclusion",
                "text": "Gross margin was 42%.",
                "evidence_refs": ["ev_2"],
            },
            ClaimCandidate(
                id="claim_3",
                type="factual_claim",
                text="The report covers Q4.",
            ),
        ],
        default_claim_type="factual_claim",
    )

    assert len(result.claims) == 3
    assert result.claims[0].type == "factual_claim"
    assert result.claims[1].id == "claim_2"
    assert result.claims[1].type == "numeric_conclusion"
    assert result.claims[2].id == "claim_3"
    assert result.skipped_items == []
    assert result.warnings == []


def test_create_claims_from_items_skips_invalid_items() -> None:
    result = create_claims_from_items(
        [
            "",
            {"claim_type": "numeric_conclusion"},
            123,
            {"text": "Revenue increased by 15%.", "claim_type": "numeric_conclusion"},
        ]
    )

    assert len(result.claims) == 1
    assert len(result.skipped_items) == 3
    assert len(result.warnings) == 3


def test_claim_extraction_template_states_boundary() -> None:
    prompt = ClaimExtractionTemplate.default().format(
        answer="Revenue increased by 15%.",
        claim_types=["numeric_conclusion"],
    )

    assert "Extraction is not verification." in prompt
    assert "Do not decide whether the claims are true." in prompt
    assert "numeric_conclusion" in prompt


def test_extraction_result_flows_into_verifier() -> None:
    extraction = create_claims_from_items(
        [
            {
                "text": "Revenue increased by 15%.",
                "claim_type": "numeric_conclusion",
                "evidence_refs": ["ev_1", "ev_2"],
            }
        ]
    )

    result = AgentClaimGuard(Policy.load_builtin("generic_numeric")).verify(
        claims=extraction.claims,
        evidence=[
            {"id": "ev_1", "type": "source_fact", "content": "Revenue was 115."},
            {"id": "ev_2", "type": "source_fact", "content": "Revenue was 100."},
        ],
        tool_results=[],
    )

    assert result.status == "blocked"
    assert result.claim_results[0].status == "tool_required"
