import logging
from google import genai
from google.genai import errors
from app.core.config import settings
from app.core.exceptions import AppException

logger = logging.getLogger(__name__)

class LLMClient:
  def __init__(self):
    self.client = genai.Client(
      api_key=settings.GEMINI_API_KEY
    )

  async def generate(self, prompt: str) -> str:
    try:
      response = await self.client.aio.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
      )

      return response.text
    except errors.APIError as e:
      logger.error(
        "Gemini API error. code=%s message=%s",
        e.code,
        e.message,
      )
      if e.code == 404:
        raise AppException(
          error_code="NOT_FOUND",
          message=e.message,
          status_code=429,
        )
      if e.code == 429:
        raise AppException(
          error_code="GEMINI_RATE_LIMIT",
          message="Gemini API rate limit exceeded. Please try again later.",
          status_code=429,
        )
      raise AppException(
        error_code="GENRIC_ERROR",
        message=e.message,
        status_code=e.code,
      )