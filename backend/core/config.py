from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Tara Digital Roadmap"
    env: str = "development"
    llm_api_key: str | None = None

    # --- Database Configuration ---
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "tara_db"
    DB_USER: str = "postgres"
    # En développement, on fournit un mot de passe par défaut pour éviter
    # que l'import du module échoue lorsque les variables d'environnement
    # ne sont pas présentes. En production, fixez `DB_PASSWORD` via .env ou
    # variables d'environnement.
    DB_PASSWORD: SecretStr = SecretStr("postgres")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # --- JWT Configuration (pour les WebSockets) ---
    # Clé secrète JWT par défaut pour dev. Remplacez en production.
    JWT_SECRET_KEY: str = "dev-jwt-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: float = 60

    # --- TARA : Configuration IA ---
    # Clés API optionnelles — elles seront lues depuis `.env` si présentes.
    # Sans valeur par défaut, Pydantic les considère comme obligatoires.
    GOOGLE_API_KEY: str | None = None
    NVIDIA_API_KEY: str | None = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
    )

try:
    settings = Settings() # type: ignore
except Exception as e:
    print(f"Warning: Failed to load settings: {e}")
    raise