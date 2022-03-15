from ast import parse
from dataclasses import dataclass
from datetime import datetime
import requests
from typing import List, Union, Dict


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
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "base_host=frenchbee.com; market_lang=en; site_origin=us.frenchbee.com",
        }

    def _make_request(
        self,
        source: str,
        destination: str,
        passengers: PassengerInfo,
        departure_date: datetime,
        module: str,
    ) -> List[FrenchBeeResponse]:
        url = "https://us.frenchbee.com/en?ajax_form=1"
        departure_date_str = f"{departure_date:%Y-%m-%d}" if departure_date else ""
        payload = {
            "visible_newsearch_flights_travel_type": "R",
            "visible_newsearch_flights_from": source,
            "visible_newsearch_flights_to": destination,
            "newsearch_flights_travel_type": "R",
            "newsearch_flights_from": source,
            "newsearch_flights_to": destination,
            "newsearch_flights_departure_date": departure_date_str,
            "adults-count": passengers.Adults,
            "children-count": passengers.Children,
            "infants-count": passengers.Infants,
            "um_youth-count": 0,
            "form_id": "frenchbee-amadeus-search-flights-form",
            "_triggering_element_name": module,
        }
        response = self.session.post(url, data=payload)
        return [FrenchBeeResponse(**i) for i in response.json()]

    def _normalize_response(self, response: dict) -> Dict[datetime, Flight]:
        if not response:
            return None
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
        return (
            self._normalize_response(info.args[1]["departure"])
            if len(info.args) < 2 or info.args[1]
            else None
        )

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
        return (
            self._normalize_response(info.args[1]["return"])
            if len(info.args) < 2 or info.args[1]
            else None
        )

    def get_departure_info_for(
        self, source: str, destination: str, passengers: PassengerInfo, date: datetime
    ) -> Flight:
        info = self.get_departure_availability(source, destination, passengers)
        return info.get(date, None) if info else None

    def get_return_info_for(
        self,
        source: str,
        destination: str,
        passengers: PassengerInfo,
        departure: datetime,
        date: datetime,
    ) -> Flight:
        info = self.get_return_availability(source, destination, passengers, departure)
        return info.get(date, None) if info else None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get French Bee airline prices.")
    parser.add_argument("origin", help="Origin airport.")
    parser.add_argument(
        "departure_date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        help="Departure date from origin airport. YYYY-mm-dd",
    )
    parser.add_argument("destination", help="Destination airport.")
    parser.add_argument(
        "return_date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        help="Return date from destination airport. YYYY-mm-dd",
    )
    parser.add_argument(
        "--passengers", type=int, default=1, help="Number of adult passengers. default=1"
    )
    parser.add_argument(
        "--children", type=int, default=0, help="Number of child passengers. default=0"
    )

    args = parser.parse_args()

    passengers = PassengerInfo(Adults=args.passengers, Children=args.children)

    client = FrenchBee()
    departure_info = client.get_departure_info_for(
        args.origin, args.destination, passengers, args.departure_date
    )
    if departure_info:
        print(departure_info)
        return_info = client.get_return_info_for(
            args.origin,
            args.destination,
            passengers,
            args.departure_date,
            args.return_date,
        )
        if return_info:
            print(return_info)
            print(
                f"Total price: ${departure_info.price + return_info.price} " +
                f"for {departure_info.day} to {return_info.day} " + 
                f"from {departure_info.departure_airport} to {return_info.departure_airport}"
            )
