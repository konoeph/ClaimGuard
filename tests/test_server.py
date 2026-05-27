from fastapi.testclient import TestClient

from claimguard.server.main import app


def test_health_endpoint() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_verify_endpoint_uses_default_policy() -> None:
    client = TestClient(app)

    response = client.post(
        "/v1/verify",
        json={
            "claims": [
                {
                    "id": "claim_1",
                    "type": "numeric_conclusion",
                    "text": "Revenue increased by 15%.",
                    "evidence_refs": ["ev_1", "ev_2"],
                    "tool_result_refs": [],
                }
            ],
            "evidence": [
                {"id": "ev_1", "type": "source_fact", "content": "Revenue was 115."},
                {"id": "ev_2", "type": "source_fact", "content": "Revenue was 100."},
            ],
            "tool_results": [],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "blocked"
    assert body["claim_results"][0]["status"] == "tool_required"

