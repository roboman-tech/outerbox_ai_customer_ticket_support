# Notes

I treated the LLM as an unreliable upstream service. The prompt asks DeepSeek for JSON output using `response_format={"type":"json_object"}`, but the API still parses the response and validates it with Pydantic before returning anything to the caller. The category and urgency fields are strict enums, so the endpoint cannot return values outside the exercise's allowed lists.

Malformed model output is handled separately from provider failures. Invalid JSON, missing fields, bad enum values, or empty content return `422`. DeepSeek timeouts, rate limits, connection errors, 5xx responses, missing API keys, and other upstream failures return `502`. Request validation errors return `400`.

Prompt injection is handled in the system prompt by explicitly marking the ticket subject and body as untrusted customer content. The user ticket is wrapped in XML-like tags and the model is instructed to ignore customer attempts to directly set the category or urgency.

One failure mode I noticed is ambiguity between `billing` and `bug_report` when a ticket says both that an invoice is wrong and that a billing page is broken. For a production version, I would add confidence scoring, human-review routing for low-confidence tickets, and a small regression eval set with expected labels.

AI tools used: ChatGPT/Codex helped scaffold the FastAPI app, write the prompt, and create validation tests. The useful part was quickly translating the exercise requirements into small files. The risk was overbuilding, so I kept persistence, auth, UI, and deployment out of scope.

