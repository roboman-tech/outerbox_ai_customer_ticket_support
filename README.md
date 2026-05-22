# AI Ticket Triage Endpoint

Small FastAPI service that accepts a support ticket and returns an LLM-generated triage result. It uses DeepSeek through the OpenAI-compatible SDK, requests JSON output from the model, and validates the result with Pydantic enums before returning it.

DeepSeek API docs used for this implementation: <https://api-docs.deepseek.com/guides/json_mode/>

Requires Python 3.11+.

## Setup

One-command setup on Windows PowerShell:

```powershell
python -m venv .venv; .\.venv\Scripts\python -m pip install -r requirements.txt; Copy-Item .env.example .env
```

Edit `.env` and set `DEEPSEEK_API_KEY`.

## Run

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```

## Sample curl

```powershell
curl.exe -X POST http://127.0.0.1:8000/triage -H "Content-Type: application/json" -d '{"ticket_id":"t-001","subject":"Cannot log in","body":"I reset my password but still cannot access my account."}'
```

Example response:

```json
{
  "category": "account_access",
  "urgency": "normal",
  "suggested_response": "Thanks for reaching out. Please try using the latest password reset link, and let us know if the issue continues.",
  "reasoning": "The ticket is about login failure after a password reset, so it fits account access. There is no sign of an outage or compromise, so normal urgency is appropriate.",
  "ticket_id": "t-001"
}
```

## Eval

With the server running:

```bash
python eval.py
```

The script sends three tickets: a clear account-access issue, an ambiguous billing/bug ticket, and a prompt-injection attempt.

## Tests

```bash
pytest
```
