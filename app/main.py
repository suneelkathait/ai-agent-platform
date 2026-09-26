from fastapi import FastAPI

from app.core.response import success_response
from app.api.v1.router import router
from app.api.routes.document import router as documents_router
from app.api.routes.search import router as search_router
from app.api.routes.chat import router as chat_router
from app.core.config import settings
from app.core.exceptions import AppException
from app.core.exception_handler import app_exception_handler
from app.core.logger import setup_logger
from app.db.mongo import check_database_connection

logger = setup_logger()

app = FastAPI(
  title=settings.APP_NAME,
  version=settings.APP_VERSION,
  description="", # if need to display description in sweger documentation 
)
app.add_exception_handler(
  AppException,
  app_exception_handler,
)

@app.get("/health")
async def health_check():
  return success_response(
    message = "ok",
    data = {
      "app_name": settings.APP_NAME,
      "database_connected": check_database_connection(),
    }
  )

app.include_router(
  router,
  prefix="/api/v1",
  tags=["AI Endpoints"]
)

app.include_router(documents_router)

app.include_router(search_router)

app.include_router(chat_router)