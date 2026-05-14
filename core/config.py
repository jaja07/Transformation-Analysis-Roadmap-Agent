from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Tara Digital Roadmap"
    env: str = "development"
    llm_api_key: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()
