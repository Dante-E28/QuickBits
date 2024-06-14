from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        env_file_encoding='utf-8'
    )


class DBSettings(EnvBaseSettings):
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    MODE: str

    @property
    def DATABASE_url_asyncpg(self) -> str:
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}'


class AuthSettings(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class RabbitMQ(EnvBaseSettings):
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int


class SMTP(EnvBaseSettings):
    SMTP_PORT: int
    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PASS: str


class Settings(DBSettings, RabbitMQ, SMTP):
    DEBUG: bool = True
    BASE_URL: str = 'http://localhost:8000'
    FRONT_URL: str = 'http://localhost:5173'

    auth_settings: AuthSettings = AuthSettings()


settings = Settings()
