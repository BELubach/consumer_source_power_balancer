from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    PROJECT_NAME: str = "FastAPI App"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = "some-secret-key-not-suitable-for-production"
    
    # Database
    APP_DB_USER: str = "postgres"
    APP_DB_PASSWORD: str = "postgres"
    APP_DB_HOST: str = "localhost"
    APP_DB_PORT: str = "5432"
    APP_DB_NAME: str = "postgres"

    SHOW_SQL: bool = False
    
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.APP_DB_USER}:{self.APP_DB_PASSWORD}"
            f"@{self.APP_DB_HOST}:{self.APP_DB_PORT}/{self.APP_DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  
    )


settings = Settings()
