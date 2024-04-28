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
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 15


class Settings(DBSettings):
    DEBUG: bool = True

    auth_settings: AuthSettings = AuthSettings()


settings = Settings()