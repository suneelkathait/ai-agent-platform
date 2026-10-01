from celery import Celery

from app.core.config import settings

REDIS_URL = settings.REDIS_URL

celery_app = Celery(
  "ai_agent_platform",
  broker=REDIS_URL,
  backend=REDIS_URL,
  include=[
    "app.worker.tasks"
  ],
)