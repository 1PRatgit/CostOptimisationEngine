from datetime import date

from pydantic import BaseModel, Field, field_validator, model_validator


class CostEstimateRequest(BaseModel):
    destination: str = Field(..., min_length=1)
    days: int = Field(..., gt=0)
    people: int = Field(..., gt=0)
    travel_mode: str = Field(default="flight", min_length=1)
    budget: str = Field(default="medium", min_length=1)

    @field_validator("destination", "travel_mode", "budget")
    @classmethod
    def normalize_text(cls, value):
        return value.strip()


class CostEstimateResponse(BaseModel):
    hotel_cost: float
    transport_cost: float
    food_cost: float
    total_cost: float
    currency: str
    breakdown: dict


class TripPricePredictionRequest(BaseModel):
    source: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)
    days: int = Field(..., gt=0)
    people: int = Field(..., gt=0)
    booking_date: date
    travel_date: date
    travel_mode: str = Field(default="flight", min_length=1)
    budget: str = Field(default="medium", min_length=1)
    day_of_week: str | None = None
    is_weekend: int | None = Field(default=None, ge=0, le=1)
    is_festival: int | None = Field(default=None, ge=0, le=1)
    season: str | None = None
    base_price: float | None = Field(default=None, gt=0)

    @field_validator("source", "destination", "travel_mode", "budget")
    @classmethod
    def normalize_required_text(cls, value):
        return value.strip()

    @field_validator("day_of_week", "season")
    @classmethod
    def normalize_optional_text(cls, value):
        return value.strip() if isinstance(value, str) else value

    @model_validator(mode="after")
    def validate_dates(self):
        if self.travel_date < self.booking_date:
            raise ValueError("travel_date must be on or after booking_date")
        return self


class TripPricePredictionResponse(BaseModel):
    predicted_price: float
    confidence: float
    reason: str
    factors: dict
    features: dict
