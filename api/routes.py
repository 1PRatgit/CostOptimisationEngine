from fastapi import APIRouter
from models.cost_models import CostEstimateRequest, CostEstimateResponse
from services.cost_service import estimate_total_cost

router = APIRouter()

@router.post("/estimate-cost", response_model=CostEstimateResponse)
async def estimate_cost(request: CostEstimateRequest):
    return estimate_total_cost(request)
