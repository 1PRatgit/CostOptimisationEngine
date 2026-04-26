import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

from core.config import settings


FLIGHT_API_URL = str(settings.FLIGHT_API_URL or settings.SKYSCANNER_API_URL or "")
FLIGHT_API_HOST = settings.FLIGHT_API_HOST or settings.SKYSCANNER_API_HOST
FLIGHT_API_KEY = settings.FLIGHT_API_KEY or settings.RAPIDAPI_HOTEL_KEY

CITY_TO_FLIGHT_ID = {
    "blr": "BLR.AIRPORT",
    "bom": "BOM.AIRPORT",
    "del": "DEL.AIRPORT",
    "goi": "GOI.AIRPORT",
    "goa": "GOI.AIRPORT",
    "par": "PAR.CITY",
    "lon": "LON.CITY",
    "mumbai": "BOM.AIRPORT",
    "bombay": "BOM.AIRPORT",
    "delhi": "DEL.AIRPORT",
    "new delhi": "DEL.AIRPORT",
    "paris": "PAR.CITY",
    "london": "LON.CITY",
    "dubai": "DXB.AIRPORT",
    "bangkok": "BKK.AIRPORT",
    "singapore": "SIN.AIRPORT",
    "bengaluru": "BLR.AIRPORT",
    "bangalore": "BLR.AIRPORT",
    "hyderabad": "HYD.AIRPORT",
    "chennai": "MAA.AIRPORT",
    "kolkata": "CCU.AIRPORT",
    "goa": "GOI.AIRPORT",
}


def _build_headers():
    return {
        "x-rapidapi-key": FLIGHT_API_KEY,
        "x-rapidapi-host": FLIGHT_API_HOST,
        "Content-Type": "application/json",
    }


def _do_rapidapi_request(url, query):
    request_url = f"{url}?{urlencode(query, quote_via=quote_plus)}"
    request = Request(request_url, headers=_build_headers())
    with urlopen(request, timeout=20) as response:
        raw = response.read().decode("utf-8")
        return json.loads(raw)


def _flight_search_destination_url():
    return FLIGHT_API_URL.replace("/getMinPrice", "/searchDestination")


def _resolve_flight_id(city_or_id):
    if not city_or_id:
        return city_or_id

    value = city_or_id.strip()
    if "." in value:
        return value.upper()

    normalized = value.lower()
    if normalized in CITY_TO_FLIGHT_ID:
        return CITY_TO_FLIGHT_ID[normalized]

    if len(value) == 3 and value.isalpha():
        return f"{value.upper()}.AIRPORT"

    payload = _do_rapidapi_request(
        _flight_search_destination_url(),
        {"query": value},
    )
    data = payload.get("data", []) if isinstance(payload, dict) else []
    if isinstance(data, dict):
        data = data.get("destinations", data.get("results", []))

    if isinstance(data, list):
        for item in data:
            if not isinstance(item, dict):
                continue
            flight_id = item.get("id") or item.get("skyId")
            if flight_id:
                return str(flight_id)

    return value


def _money_to_float(price):
    if not isinstance(price, dict):
        return None

    units = price.get("units", 0)
    nanos = price.get("nanos", 0)
    if not isinstance(units, (int, float)) or not isinstance(nanos, (int, float)):
        return None

    return float(units) + (float(nanos) / 1_000_000_000)


def _parse_min_price(payload):
    data = payload.get("data", []) if isinstance(payload, dict) else []
    if not isinstance(data, list):
        return None

    cheapest = next(
        (
            item
            for item in data
            if isinstance(item, dict) and item.get("isCheapest") is True
        ),
        None,
    )
    if cheapest:
        return _money_to_float(cheapest.get("price"))

    prices = [
        _money_to_float(item.get("price"))
        for item in data
        if isinstance(item, dict)
    ]
    prices = [price for price in prices if price is not None and price > 0]
    if not prices:
        return None

    return min(prices)


def fetch_flight_cost(destination, source=None, depart_date=None):
    if not (FLIGHT_API_URL and FLIGHT_API_HOST and FLIGHT_API_KEY):
        return None

    try:
        query = {
            "fromId": _resolve_flight_id(source or settings.DEFAULT_ORIGIN),
            "toId": _resolve_flight_id(destination),
            "departDate": depart_date or settings.DEFAULT_DEPARTURE_DATE,
            "cabinClass": settings.FLIGHT_CABIN_CLASS,
            "currency_code": settings.FLIGHT_CURRENCY_CODE,
        }

        payload = _do_rapidapi_request(FLIGHT_API_URL, query)
        return _parse_min_price(payload)
    except (HTTPError, URLError, ValueError, TypeError, KeyError):
        return None
