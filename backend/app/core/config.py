# 檔案說明: 讀取應用設定（環境、JWT secret、DB 連線、LLM 提供者/金鑰）。
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "dev"
    jwt_secret: str = "dev-secret"
    database_url: str = "sqlite:///./app.db"

    llm_provider: str = "mock"  # "mock" or "openai"
    openai_api_key: str | None = None

settings = Settings()
