from fastapi.testclient import TestClient

from app.llm import LLMOutputError
from app.main import app
from app.schemas import LLMTriageResult


def test_validation_errors_return_400() -> None:
    client = TestClient(app)

    response = client.post("/triage", json={"ticket_id": "", "subject": "", "body": ""})

    assert response.status_code == 400


def test_triage_returns_valid_structured_response(monkeypatch) -> None:
    class StubClient:
        def triage(self, ticket) -> LLMTriageResult:
            return LLMTriageResult(
                category="account_access",
                urgency="normal",
                suggested_response="Please try resetting your password again.",
                reasoning="The ticket is about login trouble after a password reset.",
            )

    monkeypatch.setattr("app.main.DeepSeekTriageClient", StubClient)
    client = TestClient(app)

    response = client.post(
        "/triage",
        json={
            "ticket_id": "t-123",
            "subject": "Cannot log in",
            "body": "The password reset did not work.",
        },
    )

    assert response.status_code == 200
    assert response.json()["ticket_id"] == "t-123"
    assert response.json()["category"] == "account_access"


def test_malformed_llm_output_returns_422(monkeypatch) -> None:
    class StubClient:
        def triage(self, ticket) -> LLMTriageResult:
            raise LLMOutputError("bad schema")

    monkeypatch.setattr("app.main.DeepSeekTriageClient", StubClient)
    client = TestClient(app)

    response = client.post(
        "/triage",
        json={
            "ticket_id": "t-123",
            "subject": "Bad model output",
            "body": "Simulate malformed JSON from the model.",
        },
    )

    assert response.status_code == 422
