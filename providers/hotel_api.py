import os
import json
from urllib.parse import urlencode, quote_plus
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from core.config import settings

RAPIDAPI_HOTEL_URL = settings.RAPIDAPI_HOTEL_URL
RAPIDAPI_HOTEL_HOST = settings.RAPIDAPI_HOTEL_HOST
RAPIDAPI_HOTEL_KEY = settings.RAPIDAPI_HOTEL_KEY


def _build_headers():
    return {
        "x-rapidapi-key": RAPIDAPI_HOTEL_KEY,
        "x-rapidapi-host": RAPIDAPI_HOTEL_HOST,
        "Content-Type": "application/json",
    }


def _parse_hotel_price(response_data):
    if not isinstance(response_data, dict):
        return None

    featured_price = (
        response_data
        .get("data", {})
        .get("body", {})
        .get("propertyDescription", {})
        .get("featuredPrice", {})
        .get("currentPrice", {})
    )
    if isinstance(featured_price, dict):
        if "plain" in featured_price and isinstance(featured_price["plain"], (int, float)):
            return float(featured_price["plain"])

    rooms = response_data.get("data", {}).get("body", {}).get("roomsAndRates", {}).get("rooms", [])
    if rooms:
        first_room = rooms[0]
        rate_plans = first_room.get("ratePlans", [])
        if rate_plans:
            price_info = rate_plans[0].get("price", {})
            if isinstance(price_info, dict):
                if "unformattedCurrent" in price_info and isinstance(price_info["unformattedCurrent"], (int, float)):
                    return float(price_info["unformattedCurrent"])
                if "current" in price_info and isinstance(price_info["current"], str):
                    try:
                        return float(price_info["current"].replace("$", ""))
                    except ValueError:
                        pass
    return None


def _do_rapidapi_request(url):
    request = Request(url, headers=_build_headers())
    with urlopen(request, timeout=15) as response:
        raw = response.read().decode("utf-8")
        return json.loads(raw)


def _resolve_property_id(destination):
    if destination and destination.isdigit():
        return destination
    return os.getenv("RAPIDAPI_HOTEL_PROPERTY_ID", "")


def fetch_hotel_cost(destination, budget, days, people):
    if not (RAPIDAPI_HOTEL_URL and RAPIDAPI_HOTEL_HOST and RAPIDAPI_HOTEL_KEY):
        return None

    property_id = _resolve_property_id(destination)
    if not property_id:
        return None

    query = {
        "id": property_id,
        "checkIn": os.getenv("HOTEL_CHECKIN_DATE", "2026-05-01"),
        "checkOut": os.getenv("HOTEL_CHECKOUT_DATE", "2026-05-02"),
        "adults1": people,
        "currency": "USD",
        "locale": "en_US",
    }
    url = f"{RAPIDAPI_HOTEL_URL}?{urlencode(query, quote_via=quote_plus)}"

    try:
        payload = _do_rapidapi_request(url)
        nightly_price = _parse_hotel_price(payload)
        if nightly_price is None:
            return None
        return nightly_price * days
    except (HTTPError, URLError, ValueError):
        return None
