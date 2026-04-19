from typing import List
from pydantic import AnyHttpUrl   
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    ALLOW_ORIGINS: List[str] = []
    SKYSCANNER_API_KEY: str
    SKYSCANNER_API_HOST: str
    SKYSCANNER_API_URL: AnyHttpUrl
    RAPIDAPI_HOTEL_KEY: str
    RAPIDAPI_HOTEL_HOST: str
    RAPIDAPI_HOTEL_URL: AnyHttpUrl  
    DEFAULT_DEPARTURE_DATE: str = "2026-05-01"

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'
        extra='forbid'
        
settings = Settings()