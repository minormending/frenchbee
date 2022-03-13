from dataclasses import dataclass
from datetime import datetime, timedelta
from pprint import pprint
import requests
from typing import List, Union, Mapping, Dict


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
    args: List[
        Union[str, dict]
    ]  # dict(departure => [year => { month => { day => { data... }} }])


@dataclass
class Flight:
    arrival_airport: str
    currency: str
    day: datetime
    departure_airport: str
    is_offer: bool
    price: float
    tax: float
    total: float


class FrenchBee:
    def _make_request(
        self,
        source: str,
        destination: str,
        passengers: PassengerInfo,
        departure_date: datetime,
        module: str,
    ) -> List[FrenchBeeResponse]:
        url = "https://us.frenchbee.com/en?ajax_form=1"
        payload = {
            "visible_newsearch_flights_travel_type": "R",
            "visible_newsearch_flights_from": source,
            "visible_newsearch_flights_to": destination,
            "newsearch_flights_travel_type": "R",
            "newsearch_flights_from": source,
            "newsearch_flights_to": destination,
            "newsearch_flights_departure_date": f"{departure_date:%Y-%m-%d}"
            if departure_date
            else "",
            "adults-count": passengers.Adults,
            "children-count": passengers.Children,
            "infants-count": passengers.Infants,
            "um_youth-count": 0,
            "form_id": "frenchbee-amadeus-search-flights-form",
            "_triggering_element_name": module,
        }
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "base_host=frenchbee.com; market_lang=en; site_origin=us.frenchbee.com",
        }
        response = session.request("POST", url, headers=headers, data=payload)
        return [FrenchBeeResponse(**i) for i in response.json()]

    def _normalize_response(self, response: dict) -> Dict[datetime, Flight]:
        normalize = {}
        for year_str, months in response.items():
            year = int(year_str)
            for month_str, days in months.items():
                month = int(month_str)
                for day_str, day_response in days.items():
                    day = int(day_str)
                    normalize[datetime(year, month, day)] = Flight(**day_response)
        return normalize

    def get_departure_availability(
        self, source: str, destination: str, passengers: PassengerInfo
    ) -> Dict[datetime, Flight]:
        payload = self._make_request(
            source,
            destination,
            passengers,
            departure_date=None,
            module="visible_newsearch_flights_to",
        )
        info = next(
            filter(lambda i: i.args[0] == "departureCalendarPriceIsReady", payload),
            None,
        )
        return self._normalize_response(info.args[1]["departure"]) if info else None

    def get_return_availability(
        self,
        source: str,
        destination: str,
        passengers: PassengerInfo,
        departure: datetime,
    ) -> Dict[datetime, Flight]:
        payload = self._make_request(
            source,
            destination,
            passengers,
            departure_date=departure,
            module="visible_newsearch_flights_departure_date",
        )
        info = next(
            filter(lambda i: i.args[0] == "returnCalendarPriceIsReady", payload), None
        )
        return self._normalize_response(info.args[1]["return"]) if info else None

    def get_departure_info_for(
        self, source: str, destination: str, passengers: PassengerInfo, date: datetime
    ) -> dict:
        info = self.get_departure_availability(source, destination, passengers)
        return info.get(date, None) if info else None

    def get_return_info_for(
        self,
        source: str,
        destination: str,
        passengers: PassengerInfo,
        departure: datetime,
        date: datetime,
    ) -> dict:
        info = self.get_return_availability(source, destination, passengers, departure)
        return info.get(date, None) if info else None


if __name__ == "__main__":
    passengers = PassengerInfo(Adults=1)
    client = FrenchBee()
    departure = client.get_departure_info_for(
        "EWR", "ORY", passengers, datetime(2022, 10, 6)
    )
    pprint(departure)

    returns = client.get_return_info_for(
        "EWR", "ORY", passengers, datetime(2022, 10, 6), datetime(2022, 10, 10)
    )
    pprint(returns)

    print(
        f"Total price: ${departure.price + returns.price} for {departure.day} to {returns.day}"
    )
