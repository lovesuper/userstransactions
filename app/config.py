from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    DATABASE_URL: str = None
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    SECRET_KEY: str = None

    class Config:
        env_file = ".env"


settings = Settings()
