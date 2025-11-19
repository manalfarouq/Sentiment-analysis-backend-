from pydantic import BaseSettings

class Settings(BaseSettings):
    HF_API_TOKEN: str
    HF_MODEL: str

    class Config:
        env_file = ".env"

settings = Settings()