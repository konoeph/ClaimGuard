from pathlib import Path

from fastapi import FastAPI

from claimguard import ClaimGuard, Policy
from claimguard.server.schemas import RepairRequest, VerifyRequest


DEFAULT_POLICY_PATH = (
    Path(__file__).resolve().parents[1] / "policies" / "generic_strict.yaml"
)

app = FastAPI(
    title="ClaimGuard",
    version="0.1.0",
    description="A framework-agnostic evidence gate for LLM claims.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/verify")
def verify(request: VerifyRequest):
    policy = request.policy or Policy.load(DEFAULT_POLICY_PATH)
    guard = ClaimGuard(policy=policy)
    return guard.verify(
        claims=request.claims,
        evidence=request.evidence,
        tool_results=request.tool_results,
    )


@app.post("/v1/repair")
def repair(request: RepairRequest):
    policy = request.policy or Policy.load(DEFAULT_POLICY_PATH)
    guard = ClaimGuard(policy=policy)
    return guard.repair(
        claims=request.claims,
        evidence=request.evidence,
        tool_results=request.tool_results,
    )

