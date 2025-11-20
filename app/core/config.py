from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SK: str
    ALG: str
    HF_API_TOKEN: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = {
        "env_file": ".env"
    }

settings = Settings()
