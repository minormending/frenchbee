from dataclasses import dataclass
from datetime import datetime


@dataclass
class PassengerInfo:
    Adults: int
    Children: int = 0
    Infants: int = 0


@dataclass
class Location:
    code: str
    name: str = None
    terminal: str = None
    transport: str = None

    def json(self) -> Dict[str, Any]:
        return minimize_dict(self.__dict__)


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


@dataclass
class DateAndLocation:
    date: datetime
    location: Location


@dataclass
class Trip:
    origin_depart: DateAndLocation
    destination_return: DateAndLocation
    passengers: PassengerInfo
