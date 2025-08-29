from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    app_password: str
    mongodb_url: str
    frontend_url: str
    email: str
    email_provider: str

    class Config:
        env_file = ".env"

settings = Settings()
