from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    CLOUD_NAME: str
    API_KEY: str
    API_SECRET: str
    SQL_ALCHEMY_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
