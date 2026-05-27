from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.llm import DeepSeekTriageClient, LLMOutputError, UpstreamLLMError
from app.schemas import TicketRequest, TriageResponse

app = FastAPI(title="AI Ticket Triage")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    # Interview note: request validation fails before the LLM is called, so bad
    # customer/API input is separated from model or provider failures.
    return JSONResponse(
        status_code=400,
        content={"detail": "Request body failed validation", "errors": exc.errors()},
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/triage", response_model=TriageResponse)
def triage(ticket: TicketRequest) -> TriageResponse:
    try:
        # Keep provider-specific work inside the client so the API route remains
        # focused on HTTP behavior and response shape.
        result = DeepSeekTriageClient().triage(ticket)
    except LLMOutputError as exc:
        return _error(422, "LLM output could not be coerced into the response schema", exc)
    except UpstreamLLMError as exc:
        return _error(502, "Upstream LLM provider failure", exc)
    except Exception as exc:
        return _error(502, "Unexpected LLM integration failure", exc)

    return TriageResponse(ticket_id=ticket.ticket_id, **result.model_dump())


def _error(status_code: int, detail: str, exc: Exception) -> JSONResponse:
    # Centralized error responses make it easy to explain the 400/422/502 split.
    return JSONResponse(
        status_code=status_code,
        content={"detail": detail, "error": str(exc)},
    )
