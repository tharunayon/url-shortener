from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Change this line back to SQLite
    DATABASE_URL: str = "sqlite:///./url_shortener.db"
    BASE_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"

settings = Settings()
