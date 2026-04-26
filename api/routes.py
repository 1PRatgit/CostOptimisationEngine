from fastapi import APIRouter
from models.cost_models import (
    CostEstimateRequest,
    CostEstimateResponse,
    TripPricePredictionRequest,
    TripPricePredictionResponse,
)
from services.cost_service import estimate_total_cost
from services.price_prediction_service import predict_trip_price

router = APIRouter()

@router.post("/estimate-cost", response_model=CostEstimateResponse)
async def estimate_cost(request: CostEstimateRequest):
    return estimate_total_cost(request)


@router.post("/predict-price", response_model=TripPricePredictionResponse)
async def predict_price(request: TripPricePredictionRequest):
    return predict_trip_price(request)
