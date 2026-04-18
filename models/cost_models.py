from pydantic import BaseModel

class CostEstimateRequest(BaseModel):
    destination: str
    days: int
    people: int
    travel_mode: str
    budget: str

class CostEstimateResponse(BaseModel):
    hotel_cost: float
    transport_cost: float
    food_cost: float
    total_cost: float
    currency: str
    breakdown: dict
