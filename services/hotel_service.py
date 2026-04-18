HOTEL_PRICE = {
    "low": 1000,
    "medium": 2500,
    "high": 6000
}

def estimate_hotel_cost(days, people, budget):
    base = HOTEL_PRICE[budget]
    return base * days * (1 if people <= 2 else people / 2)
