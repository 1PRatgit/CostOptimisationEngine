def estimate_transport(destination, mode):
    base_prices = {
        "flight": 4000,
        "train": 800,
        "bus": 1200,
        "car": 2000
    }
    return base_prices.get(mode, 1500)
