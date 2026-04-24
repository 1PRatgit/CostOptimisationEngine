from typing import List
from pydantic import AnyHttpUrl   
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    ALLOW_ORIGINS: List[str] = []
    SKYSCANNER_API_KEY: str = ""
    SKYSCANNER_API_HOST: str = ""
    SKYSCANNER_API_URL: AnyHttpUrl | None = None
    FLIGHT_API_KEY: str = ""
    FLIGHT_API_HOST: str = ""
    FLIGHT_API_URL: AnyHttpUrl | None = None
    RAPIDAPI_HOTEL_KEY: str
    RAPIDAPI_HOTEL_HOST: str
    RAPIDAPI_HOTEL_URL: AnyHttpUrl  
    RAPIDAPI_HOTEL_SEARCH_URL: AnyHttpUrl | None = None
    RAPIDAPI_HOTEL_PROPERTY_ID: str = ""
    HOTEL_CHECKIN_DATE: str = "2026-05-01"
    HOTEL_CHECKOUT_DATE: str | None = None
    HOTEL_CURRENCY: str = "AED"
    HOTEL_LOCATION: str = "US"
    DEFAULT_ORIGIN: str = "BOM.AIRPORT"
    DEFAULT_DEPARTURE_DATE: str = "2026-05-01"
    FLIGHT_ADULTS: int = 1
    FLIGHT_CURRENCY_CODE: str = "AED"
    FLIGHT_CABIN_CLASS: str = "ECONOMY"

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'
        extra='forbid'
        
settings = Settings()
