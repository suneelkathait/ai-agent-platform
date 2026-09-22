import logging
from fastapi import APIRouter

from google.genai import errors
from app.core.response import success_response
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.core.exceptions import AppException

router = APIRouter()

logger = logging.getLogger(__name__)

chat_service = ChatService()

@router.get("/health")
async def health_check():
  return success_response(
    message = "ok",
    data = "ai-agent-platform",
  )

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
  logger.info("Normal application information")
  try:
    answer = await chat_service.chat(request.question)

    return ChatResponse(
      answer=answer
    )
 
    # return success_response(
    #   message="AI Response successfully",
    #   data=ChatResponse(
    #     answer=answer
    #   ),
    # )
  except errors.APIError as e:
    logger.error(
      "Gemini API error. code=%s message=%s",
      e.code,
      e.message,
    )
    raise AppException(
      error_code="AI_API_ERROR",
      message="AI service failed",
      status_code=500,
  )
