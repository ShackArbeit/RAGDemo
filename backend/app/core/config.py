from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "dev"
    jwt_secret: str = "dev-secret"
    database_url: str = "sqlite:///./app.db"

    llm_provider: str = "mock"  # "mock" or "openai"
    openai_api_key: str | None = None

settings = Settings()