from collections.abc import Iterable

from pydantic import BaseModel


DEFAULT_CLAIM_EXTRACTION_TEMPLATE = """You extract claim candidates from an LLM/RAG/Agent answer.

Extraction is not verification.
Do not decide whether the claims are true.
Only identify claim-like statements that should later be checked against
evidence, tool results, and policy.

Answer:
{answer}

Context:
{context}

Preferred claim types:
{claim_types}

Return JSON with this shape:

{{
  "claims": [
    {{
      "text": "claim text",
      "type": "numeric_conclusion | compliance_judgment | factual_claim | general",
      "verdict": null,
      "evidence_refs": [],
      "tool_result_refs": [],
      "confidence": null,
      "metadata": {{}}
    }}
  ]
}}
"""


class ClaimExtractionTemplate(BaseModel):
    template: str

    @classmethod
    def default(cls) -> "ClaimExtractionTemplate":
        return cls(template=DEFAULT_CLAIM_EXTRACTION_TEMPLATE)

    def format(
        self,
        *,
        answer: str,
        context: str | None = None,
        claim_types: Iterable[str] | None = None,
    ) -> str:
        claim_type_text = ", ".join(claim_types or ["general"])
        return self.template.format(
            answer=answer,
            context=context or "(none provided)",
            claim_types=claim_type_text,
        )
