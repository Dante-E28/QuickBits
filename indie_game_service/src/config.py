from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    MODE: str

    @property
    def DATABASE_url_asyncpg(self) -> str:
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}'


settings = Settings()
