from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(
  settings.MONGODB_URL,
  serverSelectionTimeoutMS=3000,
)
database = client[settings.DATABASE_NAME]
documents_collection = database["documents"]

def check_database_connection():
  try:
    client.admin.command("ping")
    return True
  except Exception:
    return False