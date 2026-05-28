import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentclaimguard import AgentClaimGuard, Policy  # noqa: E402


def chunk_to_evidence(chunk: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "id": f"ev_chunk_{index}",
        "type": "source_fact",
        "source": chunk.get("document_name"),
        "locator": f"{chunk.get('document_id')}#{chunk.get('id')}",
        "content": chunk["content"],
        "metadata": {
            "provider": "ragflow",
            "chunk_id": chunk.get("id"),
            "document_id": chunk.get("document_id"),
            "score": chunk.get("score"),
            "page": chunk.get("page"),
        },
    }


def main() -> None:
    here = Path(__file__).resolve().parent
    chunks = json.loads((here / "retrieved_chunks.json").read_text(encoding="utf-8"))
    evidence = [
        chunk_to_evidence(chunk, index)
        for index, chunk in enumerate(chunks, start=1)
    ]

    claims = [
        {
            "id": "claim_ragflow_1",
            "text": "Revenue increased by 15%.",
            "type": "numeric_conclusion",
            "evidence_refs": [item["id"] for item in evidence],
        }
    ]

    result = AgentClaimGuard(Policy.load_builtin("generic_numeric")).verify(
        claims=claims,
        evidence=evidence,
        tool_results=[],
    )

    print(f"retrieved_chunks={len(chunks)}")
    print(f"mapped_evidence={len(evidence)}")
    print(f"first_locator={evidence[0]['locator']}")
    print(f"guard_status={result.status}")
    print(f"claim_status={result.claim_results[0].status}")
    print(f"safe_verdict={result.claim_results[0].safe_verdict}")


if __name__ == "__main__":
    main()
