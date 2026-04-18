from services.hotel_service import estimate_hotel_cost
from services.transport_service import estimate_transport
from services.food_service import estimate_food
from utils.currency import get_currency

def estimate_total_cost(data):
    hotel = estimate_hotel_cost(data.days, data.people, data.budget)
    transport = estimate_transport(data.destination, data.travel_mode)
    food = estimate_food(data.days, data.people, data.budget)

    total = hotel + transport + food

    per_day = total / data.days
    per_person = total / data.people

    return {
        "hotel_cost": hotel,
        "transport_cost": transport,
        "food_cost": food,
        "total_cost": total,
        "currency": get_currency(),
        "breakdown": {
            "per_day": per_day,
            "per_person": per_person
        }
    }