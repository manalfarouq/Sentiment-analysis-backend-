from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SK: str
    ALG: str
    HF_API_TOKEN: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    DB_HOST: str 
    DB_PORT: int 
    DB_NAME: str 
    DB_USER: str 
    DB_PASSWORD: str 
    
    model_config = {
        "env_file": ".env"
    }

settings = Settings()
