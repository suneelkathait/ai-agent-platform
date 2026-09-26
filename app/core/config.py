from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  APP_NAME: str = "AI Knowledge & Task Agent Platform"
  APP_VERSION: str = "1.0.0"
  ENVIRONMENT: str = "development"

  GEMINI_API_KEY: str

  MONGODB_URL: str
  DATABASE_NAME: str

  REDIS_URL: str
  VECTOR_DB_URL: str

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
  )

settings = Settings()