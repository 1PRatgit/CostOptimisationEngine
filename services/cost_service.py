from services.food_service import estimate_food
from services.hotel_service import estimate_hotel_cost
from services.transport_service import estimate_transport
from utils.currency import get_currency


def _as_cost(value):
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def estimate_total_cost(data):
    hotel_cost = _as_cost(
        estimate_hotel_cost(data.days, data.people, data.budget, data.destination)
    )
    transport_cost = _as_cost(
        estimate_transport(data.destination, data.travel_mode)
    )
    food_cost = _as_cost(
        estimate_food(data.days, data.people, data.budget)
    )

    total_cost = hotel_cost + transport_cost + food_cost

    return {
        "hotel_cost": hotel_cost,
        "transport_cost": transport_cost,
        "food_cost": food_cost,
        "total_cost": total_cost,
        "currency": get_currency(),
        "breakdown": {
            "per_day": total_cost / int(data.days),
            "per_person": total_cost / int(data.people),
        },
    }
