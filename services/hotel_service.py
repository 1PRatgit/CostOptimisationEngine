from providers.hotel_api import fetch_hotel_cost
from services.food_service import normalize_budget


HOTEL_PRICE_PER_NIGHT = {
    "low": 1000,
    "medium": 2500,
    "high": 6000,
}


def _fallback_hotel_cost(days, people, budget):
    budget = normalize_budget(budget)
    rooms = max(1, (int(people) + 1) // 2)
    return HOTEL_PRICE_PER_NIGHT[budget] * int(days) * rooms


def estimate_hotel_cost(days, people, budget, destination):
    api_cost = fetch_hotel_cost(destination, budget, days, people)
    if isinstance(api_cost, (int, float)) and api_cost > 0:
        return float(api_cost)

    return float(_fallback_hotel_cost(days, people, budget))
