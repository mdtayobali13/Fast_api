from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_username: str
    database_password: str
    database_name: str
    database_key: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Pydantic v2 uses `model_config` instead of inner `Config` class
    model_config = {
        "env_file": ".env"
    }

settings = Settings()