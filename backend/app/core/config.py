"""
Configuración global de la aplicación usando Pydantic Settings.
Carga variables de entorno automáticamente desde .env
"""

from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

# Encontrar el directorio root del proyecto (2 niveles arriba desde este archivo)
# Este archivo: /backend/app/core/config.py
# Root: /backend/app/core -> /backend/app -> /backend -> /root
ROOT_DIR = Path(__file__).parent.parent.parent.parent
ENV_FILE_PATH = ROOT_DIR / ".env"


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # Project Info
    PROJECT_NAME: str = "MemoryCard API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str
    DATABASE_URL_SYNC: str  # Para Alembic (no soporta async)

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # RAWG API
    RAWG_API_KEY: str
    RAWG_BASE_URL: str = "https://api.rawg.io/api"

    # CORS (string separado por comas, será convertido a lista)
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> List[str]:
        """Convierte string separado por comas en lista"""
        if isinstance(self.ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
        return self.ALLOWED_ORIGINS

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

settings = Settings()
