from providers.transport_api import fetch_flight_cost


TRANSPORT_PRICE = {
    "flight": 4000,
    "train": 1500,
    "bus": 800,
    "car": 2500,
}


def normalize_travel_mode(travel_mode):
    if not isinstance(travel_mode, str):
        return "flight"

    normalized = travel_mode.strip().lower()
    if normalized in TRANSPORT_PRICE:
        return normalized

    return "flight"


def estimate_transport(destination, travel_mode, source=None, depart_date=None):
    travel_mode = normalize_travel_mode(travel_mode)

    if travel_mode == "flight":
        api_cost = fetch_flight_cost(destination, source=source, depart_date=depart_date)
        if isinstance(api_cost, (int, float)) and api_cost > 0:
            return float(api_cost)

    return float(TRANSPORT_PRICE[travel_mode])
