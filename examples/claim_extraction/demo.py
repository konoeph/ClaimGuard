import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentclaimguard import AgentClaimGuard, Policy  # noqa: E402
from agentclaimguard.extractors import (  # noqa: E402
    ClaimExtractionTemplate,
    create_claims_from_items,
)


def main() -> None:
    answer = "Revenue increased by 15%."
    template = ClaimExtractionTemplate.default()
    _prompt = template.format(
        answer=answer,
        claim_types=["numeric_conclusion", "factual_claim"],
    )

    extraction = create_claims_from_items(
        [
            {
                "text": answer,
                "claim_type": "numeric_conclusion",
                "evidence_refs": ["ev_1", "ev_2"],
            },
            {"claim_type": "numeric_conclusion"},
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

    print(f"extracted_claims={len(extraction.claims)}")
    print(f"skipped_items={len(extraction.skipped_items)}")
    print(f"guard_status={result.status}")
    print(f"claim_status={result.claim_results[0].status}")
    print(f"safe_verdict={result.claim_results[0].safe_verdict}")


if __name__ == "__main__":
    main()
