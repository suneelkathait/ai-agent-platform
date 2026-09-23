import logging
import time

from google import genai
from google.genai import errors

from app.core.config import settings
from app.core.exceptions import AppException
from app.llm.client2 import generate_AI_answer

logger = logging.getLogger(__name__)

client = genai.Client(
  api_key=settings.GEMINI_API_KEY
)

def generate_answer(
  question: str,
  context: str
) -> str:

  prompt = f"""
  You are a helpful AI assistant.

  Answer the user's question using only the information
  provided in the context.

  If the answer cannot be found in the context,
  say that the information is not available in the
  provided documents.

  Context:
  {context}

  User Question:
  {question}

  Answer:
  """

  # Retry temporary Gemini failures
  max_retries = 3

  for attempt in range(max_retries):
    try:
      response = generate_AI_answer(prompt)
      return response.text

    except errors.APIError as e:
      logger.error(
        "Gemini API error. attempt=%s code=%s message=%s",
        attempt + 1,
        e.code,
        e.message,
      )

      # Rate limit
      if e.code == 429:
        raise AppException(
          error_code="GEMINI_RATE_LIMIT",
          message="Gemini API rate limit exceeded. Please try again later.",
          status_code=429,
        )

      # Temporary Gemini server overload
      if e.code == 503:
        if attempt < max_retries - 1:
          wait_time = 2 ** attempt

          logger.warning(
            "Gemini temporarily unavailable. "
            "Retrying in %s seconds...",
            wait_time,
          )

          time.sleep(wait_time)
          continue

        raise AppException(
          error_code="GEMINI_UNAVAILABLE",
          message="Gemini is temporarily unavailable. Please try again.",
          status_code=503,
        )

      # Other Gemini API errors
      raise AppException(
        error_code="GEMINI_API_ERROR",
        message="Gemini API request failed.",
        status_code=502,
      )

    except Exception:
      raise AppException(
        error_code="GEMINI_INTERNAL_ERROR",
        message="An unexpected error occurred while generating the answer.",
        status_code=500,
      )
