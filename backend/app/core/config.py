from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn

class Settings(BaseSettings):
    # Application settings
    PROJECT_NAME: str = Field("Inventory Management", env="PROJECT_NAME")
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: PostgresDsn = Field(..., env="DATABASE_URL")

    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = Field(["*"], env="BACKEND_CORS_ORIGINS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
