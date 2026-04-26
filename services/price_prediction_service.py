from services.food_service import estimate_food
from services.hotel_service import estimate_hotel_cost
from services.transport_service import estimate_transport


NATIONAL_FESTIVALS = {
    "2026-01-01": "New Year's Day",
    "2026-01-26": "Republic Day",
    "2026-03-04": "Holi",
    "2026-03-21": "Id-ul-Fitr",
    "2026-03-26": "Ram Navami",
    "2026-04-03": "Good Friday",
    "2026-05-01": "Buddha Purnima",
    "2026-05-27": "Id-ul-Zuha",
    "2026-06-26": "Muharram",
    "2026-08-15": "Independence Day",
    "2026-08-26": "Id-e-Milad",
    "2026-09-04": "Janmashtami",
    "2026-10-02": "Mahatma Gandhi's Birthday",
    "2026-10-20": "Dussehra",
    "2026-11-08": "Diwali",
    "2026-11-24": "Guru Nanak's Birthday",
    "2026-12-25": "Christmas",
}

REGIONAL_FESTIVALS = {
    "bangalore": {
        "2026-01-15": "Makara Sankranti",
        "2026-03-19": "Ugadi",
        "2026-04-20": "Basava Jayanti",
    },
    "bengaluru": {
        "2026-01-15": "Makara Sankranti",
        "2026-03-19": "Ugadi",
        "2026-04-20": "Basava Jayanti",
    },
    "hyderabad": {
        "2026-01-15": "Makara Sankranti",
        "2026-03-19": "Ugadi",
        "2026-04-20": "Akshaya Tritiya",
    },
    "chennai": {
        "2026-01-15": "Makara Sankranti",
        "2026-04-14": "Tamil New Year",
        "2026-04-20": "Akshaya Tritiya",
    },
    "kochi": {
        "2026-01-15": "Makara Sankranti",
        "2026-04-14": "Vishu",
        "2026-04-20": "Akshaya Tritiya",
    },
    "goa": {
        "2026-01-01": "New Year's Day",
        "2026-12-25": "Christmas",
    },
    "delhi": {
        "2026-11-08": "Diwali",
    },
}

LOCATION_DEMAND = {
    "goa": 0.20,
    "mumbai": 0.14,
    "delhi": 0.12,
    "new delhi": 0.12,
    "bangalore": 0.10,
    "bengaluru": 0.10,
    "paris": 0.18,
    "dubai": 0.16,
    "london": 0.16,
}


def get_season(month):
    if month in [11, 12, 1]:
        return "winter"
    if month in [3, 4, 5]:
        return "summer"
    return "monsoon"


def _festival_name(destination, travel_date):
    date_key = travel_date.isoformat()
    destination_key = destination.strip().lower()

    regional = REGIONAL_FESTIVALS.get(destination_key, {})
    if date_key in regional:
        return regional[date_key]

    return NATIONAL_FESTIVALS.get(date_key)


def build_features(data):
    travel_date = data.travel_date
    booking_date = data.booking_date
    day_of_week = data.day_of_week or travel_date.strftime("%A")
    season = (data.season or get_season(travel_date.month)).lower()
    festival_name = _festival_name(data.destination, travel_date)

    is_weekend = (
        data.is_weekend
        if data.is_weekend is not None
        else int(day_of_week in ["Saturday", "Sunday"])
    )
    is_festival = (
        data.is_festival
        if data.is_festival is not None
        else int(festival_name is not None)
    )

    lead_time = (travel_date - booking_date).days
    destination_key = data.destination.strip().lower()

    return {
        "source": data.source.upper(),
        "destination": data.destination.upper(),
        "days": int(data.days),
        "people": int(data.people),
        "lead_time": lead_time,
        "day_of_week": day_of_week,
        "is_weekend": int(is_weekend),
        "is_festival": int(is_festival),
        "festival_name": festival_name,
        "season": season,
        "location_demand": LOCATION_DEMAND.get(destination_key, 0.08),
    }


def _base_price(data):
    if data.base_price is not None:
        return float(data.base_price)

    hotel_cost = estimate_hotel_cost(
        data.days,
        data.people,
        data.budget,
        data.destination,
    )
    transport_cost = estimate_transport(
        data.destination,
        data.travel_mode,
        source=data.source,
        depart_date=data.travel_date.isoformat(),
    )
    food_cost = estimate_food(data.days, data.people, data.budget)
    return float(hotel_cost) + float(transport_cost) + float(food_cost)


def _season_adjustment(destination, season):
    destination_key = destination.strip().lower()
    if destination_key == "goa":
        return {"winter": 0.25, "summer": 0.12, "monsoon": -0.08}.get(season, 0.0)
    if destination_key in ["delhi", "new delhi"]:
        return {"winter": 0.15, "summer": -0.04, "monsoon": -0.02}.get(season, 0.0)
    return {"winter": 0.10, "summer": 0.08, "monsoon": -0.03}.get(season, 0.0)


def _lead_time_adjustment(lead_time):
    if lead_time <= 7:
        return 0.20
    if lead_time <= 14:
        return 0.10
    if lead_time >= 60:
        return -0.08
    return 0.0


def _format_percent(value):
    sign = "+" if value >= 0 else ""
    return f"{sign}{round(value * 100)}%"


def _confidence(features, total_adjustment, used_base_price):
    confidence = 0.78
    if used_base_price:
        confidence += 0.06
    if features["lead_time"] < 7:
        confidence -= 0.08
    if abs(total_adjustment) > 0.50:
        confidence -= 0.06
    if features["is_festival"]:
        confidence -= 0.03
    return round(max(0.55, min(confidence, 0.90)), 2)


def predict_trip_price(data):
    features = build_features(data)
    base_price = _base_price(data)

    adjustments = {
        "weekend": 0.15 if features["is_weekend"] else 0.0,
        "festival": 0.25 if features["is_festival"] else 0.0,
        "low_lead_time": _lead_time_adjustment(features["lead_time"]),
        "seasonality": _season_adjustment(data.destination, features["season"]),
        "location_demand": features["location_demand"],
    }

    multiplier = 1 + sum(adjustments.values())
    predicted_price = round(base_price * multiplier, 2)

    active_factors = {
        key: _format_percent(value)
        for key, value in adjustments.items()
        if value != 0
    }

    reason_parts = [
        f"Base trip price was adjusted by {', '.join(active_factors.keys()) or 'no major demand factors'}."
    ]
    if features["festival_name"]:
        reason_parts.append(f"Festival/event detected: {features['festival_name']}.")
    reason_parts.append(
        f"Lead time is {features['lead_time']} days and season is {features['season']}."
    )

    return {
        "predicted_price": predicted_price,
        "confidence": _confidence(
            features,
            sum(adjustments.values()),
            data.base_price is not None,
        ),
        "reason": " ".join(reason_parts),
        "factors": active_factors,
        "features": {
            **features,
            "base_price": round(base_price, 2),
            "multiplier": round(multiplier, 2),
        },
    }
