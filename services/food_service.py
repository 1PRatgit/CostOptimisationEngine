FOOD_PRICE_PER_PERSON_PER_DAY = {
    "low": 400,
    "medium": 700,
    "high": 1200,
}


def normalize_budget(budget):
    if not isinstance(budget, str):
        return "medium"

    normalized = budget.strip().lower()
    if normalized in FOOD_PRICE_PER_PERSON_PER_DAY:
        return normalized

    return "medium"


def estimate_food(days, people, budget):
    budget = normalize_budget(budget)
    return FOOD_PRICE_PER_PERSON_PER_DAY[budget] * int(days) * int(people)
