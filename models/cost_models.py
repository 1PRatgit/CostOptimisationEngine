from pydantic import BaseModel, Field, field_validator


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
