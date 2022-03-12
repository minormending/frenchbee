from dataclasses import dataclass
from datetime import datetime, timedelta
from pprint import pprint
import requests
from typing import List, Union, Mapping


from requests_cache import CachedSession


session = CachedSession(
    cache_name="frenchbee_cache",
    backend="filesystem",
    use_cache_dir=True,
    expire_after=timedelta(days=1),
)


@dataclass
class PassengerInfo:
    Adults: int
    Children: int = 0
    Infants: int = 0

@dataclass
class FrenchBeeResponse:
    command: str
    selector: str
    method: str
    args: List[Union[str, dict]] # dict(departure => [year => { month => { day => { data... }} }])



def get_frenchbee_departure(
    source: str, destination: str, passengers: PassengerInfo
) -> List[FrenchBeeResponse]:
    url = "https://us.frenchbee.com/en?ajax_form=1"
    payload = {
        "visible_newsearch_flights_travel_type": "R",
        "visible_newsearch_flights_from": source,
        "visible_newsearch_flights_to": destination,
        "adults-count": passengers.Adults,
        "children-count": passengers.Children,
        "infants-count": passengers.Infants,
        "um_youth-count": 0,
        "form_id": "frenchbee-amadeus-search-flights-form",
        "_triggering_element_name": "visible_newsearch_flights_to",
    }
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "base_host=frenchbee.com; market_lang=en; site_origin=us.frenchbee.com",
    }
    response = session.request("POST", url, headers=headers, data=payload)
    return [FrenchBeeResponse(**i) for i in response.json()]


def get_departure_info_for(source: str, destination: str, passengers: PassengerInfo, date: datetime) -> dict:
    payload = get_frenchbee_departure(source, destination, passengers)
    info = next(filter(lambda i: i.args[0] == 'departureCalendarPriceIsReady', payload), None)
    if not info: return None
    info = info.args[1]['departure']
    return info.get(str(date.year), {}).get(f"{date:%m}", {}).get(f"{date:%d}", {})

    

passengers = PassengerInfo(Adults=1)
prices = get_departure_info_for("EWR", "ORY", passengers, datetime(2022,10,6))
pprint(prices)
