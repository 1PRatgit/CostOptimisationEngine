from providers.transport_api import fetch_flight_cost

BASE_TRANSPORT_COSTS = {
    "flight": 4000,
    "train": 800,
    "bus": 1200,
    "car": 2000
}


def estimate_transport(destination, mode):
    if mode == "flight":
        api_cost = fetch_flight_cost(destination)
        if api_cost is not None:
            return api_cost
    return BASE_TRANSPORT_COSTS.get(mode, 1500)
