import os
import json
from urllib.parse import urlencode, quote_plus
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from core.config import settings

SKYSCANNER_API_URL = settings.SKYSCANNER_API_URL
SKYSCANNER_API_HOST = settings.SKYSCANNER_API_HOST
SKYSCANNER_API_KEY = settings.SKYSCANNER_API_KEY


def _build_headers():
    return {
        "X-RapidAPI-Key": SKYSCANNER_API_KEY,
        "X-RapidAPI-Host": SKYSCANNER_API_HOST,
        "Accept": "application/json",
    }


def _parse_flight_price(response_data):
    if isinstance(response_data, dict):
        for key in ("price", "fare", "min_price", "price_total", "total_price"):
            if key in response_data and isinstance(response_data[key], (int, float)):
                return float(response_data[key])
        if "data" in response_data and isinstance(response_data["data"], list) and response_data["data"]:
            first = response_data["data"][0]
            if isinstance(first, dict):
                for key in ("price", "fare", "min_price", "price_total"):
                    if key in first and isinstance(first[key], (int, float)):
                        return float(first[key])
        if "itineraries" in response_data and isinstance(response_data["itineraries"], list) and response_data["itineraries"]:
            first_itinerary = response_data["itineraries"][0]
            if isinstance(first_itinerary, dict) and "price" in first_itinerary and isinstance(first_itinerary["price"], (int, float)):
                return float(first_itinerary["price"])
    return None


def _do_rapidapi_request(url):
    request = Request(url, headers=_build_headers())
    with urlopen(request, timeout=15) as response:
        raw = response.read().decode("utf-8")
        return json.loads(raw)


def fetch_flight_cost(destination):
    if not (SKYSCANNER_API_URL and SKYSCANNER_API_HOST and SKYSCANNER_API_KEY):
        return None

    query = {
        "destination": destination,
        "currency": "INR",
        "adults": 1,
        "cabin_class": "economy",
        "page_size": 1,
    }
    url = f"{SKYSCANNER_API_URL}?{urlencode(query, quote_via=quote_plus)}"

    try:
        payload = _do_rapidapi_request(url)
        return _parse_flight_price(payload)
    except (HTTPError, URLError, ValueError):
        return None
