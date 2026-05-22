from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Category(StrEnum):
    BILLING = "billing"
    ACCOUNT_ACCESS = "account_access"
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"
    OTHER = "other"


class Urgency(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class TicketRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    ticket_id: str = Field(..., min_length=1, max_length=128)
    subject: str = Field(..., min_length=1, max_length=300)
    body: str = Field(..., min_length=1, max_length=8000)


class LLMTriageResult(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    category: Category
    urgency: Urgency
    suggested_response: str = Field(..., min_length=1, max_length=1200)
    reasoning: str = Field(..., min_length=1, max_length=600)


class TriageResponse(LLMTriageResult):
    ticket_id: str

