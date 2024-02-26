# app/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str

settings = Settings()