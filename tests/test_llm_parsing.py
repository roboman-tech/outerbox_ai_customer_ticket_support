import pytest

from app.llm import LLMOutputError, parse_llm_result


def test_parse_llm_result_accepts_valid_json() -> None:
    result = parse_llm_result(
        """
        {
          "category": "account_access",
          "urgency": "normal",
          "suggested_response": "Thanks for reaching out. Please try another reset link.",
          "reasoning": "The user cannot log in after a password reset, so this is account access."
        }
        """
    )

    assert result.category == "account_access"
    assert result.urgency == "normal"


def test_parse_llm_result_normalizes_enum_case() -> None:
    result = parse_llm_result(
        """
        {
          "category": " Billing ",
          "urgency": " HIGH ",
          "suggested_response": "We will review the invoice discrepancy.",
          "reasoning": "The request concerns an invoice and billing page."
        }
        """
    )

    assert result.category == "billing"
    assert result.urgency == "high"


def test_parse_llm_result_rejects_invalid_category() -> None:
    with pytest.raises(LLMOutputError):
        parse_llm_result(
            """
            {
              "category": "refund",
              "urgency": "normal",
              "suggested_response": "We will help.",
              "reasoning": "Invalid category should be rejected."
            }
            """
        )

