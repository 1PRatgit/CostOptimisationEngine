from providers.hotel_api import fetch_hotel_cost

HOTEL_PRICE = {
    "low": 1000,
    "medium": 2500,
    "high": 6000
}


def _fallback_hotel_cost(days, people, budget):
    base = HOTEL_PRICE.get(budget, HOTEL_PRICE["medium"])
    return base * days * (1 if people <= 2 else people / 2)


def estimate_hotel_cost(days, people, budget, destination):
    api_cost = fetch_hotel_cost(destination, budget, days, people)
    if api_cost is not None:
        return api_cost
    return _fallback_hotel_cost(days, people, budget)
