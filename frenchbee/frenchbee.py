from dataclasses import dataclass
from datetime import datetime
from requests import Session, Response
from typing import Any, List, Union, Dict

from .models import PassengerInfo, Flight




@dataclass
class FrenchBeeResponse:
    command: str
    selector: str
    method: str
    args: List[
        Union[str, dict]
    ]  # dict(departure => [year => { month => { day => { data... }} }])


class FrenchBee:
    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "base_host=frenchbee.com; market_lang=en; site_origin=us.frenchbee.com",
        }

    def _make_search_request(
        self,
        source: str,
        destination: str,
        passengers: PassengerInfo,
        departure: datetime,
        module: str,
    ) -> List[FrenchBeeResponse]:
        url: str = "https://us.frenchbee.com/en?ajax_form=1"
        departure_date: str = f"{departure:%Y-%m-%d}" if departure else ""
        payload: Dict[str, str] = {
            "visible_newsearch_flights_travel_type": "R",
            "visible_newsearch_flights_from": source,
            "visible_newsearch_flights_to": destination,
            "newsearch_flights_travel_type": "R",
            "newsearch_flights_from": source,
            "newsearch_flights_to": destination,
            "newsearch_flights_departure_date": departure_date,
            "adults-count": passengers.Adults,
            "children-count": passengers.Children,
            "infants-count": passengers.Infants,
            "um_youth-count": 0,
            "form_id": "frenchbee-amadeus-search-flights-form",
            "_triggering_element_name": module,
        }
        response: Response = self.session.post(url, data=payload)
        return [FrenchBeeResponse(**i) for i in response.json()]

    def _normalize_response(self, response: Dict[str, Any]) -> Dict[datetime, Flight]:
        if not response:
            return None
        normalize: Dict[datetime, Flight] = {}
        for (
            key_year,
            months,
        ) in (
            response.items()
        ):  # key_year: str, months: Dict[str, Dict[str, Dict[str, Any]]]
            year: int = int(key_year)
            for (
                key_month,
                days,
            ) in months.items():  # key_month: str, days: Dict[str, Dict[str, Any]]
                month: int = int(key_month)
                for (
                    key_day,
                    flight,
                ) in days.items():  # key_day: str, flight: Dict[str, Any]
                    day: int = int(key_day)
                    normalize[datetime(year, month, day)] = Flight(**flight)
        return normalize

    def get_departure_availability(
        self, source: str, destination: str, passengers: PassengerInfo
    ) -> Dict[datetime, Flight]:
        payload: List[FrenchBeeResponse] = self._make_search_request(
            source,
            destination,
            passengers,
            departure=None,
            module="visible_newsearch_flights_to",
        )
        info: FrenchBeeResponse = next(
            filter(lambda r: r.args[0] == "departureCalendarPriceIsReady", payload),
            None,
        )
        return (
            self._normalize_response(info.args[1].get("departure"))
            if len(info.args) >= 2 and info.args[1]
            else None
        )

    def get_return_availability(
        self,
        source: str,
        destination: str,
        passengers: PassengerInfo,
        departure: datetime,
    ) -> Dict[datetime, Flight]:
        payload: List[FrenchBeeResponse] = self._make_search_request(
            source,
            destination,
            passengers,
            departure=departure,
            module="visible_newsearch_flights_departure_date",
        )
        info: FrenchBeeResponse = next(
            filter(lambda i: i.args[0] == "returnCalendarPriceIsReady", payload), None
        )
        return (
            self._normalize_response(info.args[1].get("return"))
            if len(info.args) >= 2 and info.args[1]
            else None
        )

    def get_departure_info_for(
        self, source: str, destination: str, passengers: PassengerInfo, date: datetime
    ) -> Flight:
        info: Dict[datetime, Flight] = self.get_departure_availability(
            source, destination, passengers
        )
        return info.get(date) if info else None

    def get_return_info_for(
        self,
        source: str,
        destination: str,
        passengers: PassengerInfo,
        departure: datetime,
        date: datetime,
    ) -> Flight:
        info: Dict[datetime, Flight] = self.get_return_availability(
            source, destination, passengers, departure
        )
        return info.get(date) if info else None
