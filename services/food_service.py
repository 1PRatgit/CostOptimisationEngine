FOOD_COST = {
    "low": 300,
    "medium": 700,
    "high": 1500
}

def estimate_food(days, people, budget):
    return budget * days * people