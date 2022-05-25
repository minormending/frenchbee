from dataclasses import dataclass
from datetime import datetime


@dataclass
class PassengerInfo:
    Adults: int
    Children: int = 0
    Infants: int = 0


@dataclass
class Airport:
    code: str
    name: str


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
