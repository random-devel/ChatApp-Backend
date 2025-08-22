from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    app_password: str

    class Config:
        env_file = ".env"

settings = Settings()
