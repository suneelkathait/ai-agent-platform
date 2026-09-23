from google import genai

from app.core.config import settings

client = genai.Client(
  api_key=settings.GEMINI_API_KEY
)

def generate_AI_answer(
  prompt: str,
) -> str:

  return client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
  )

   
