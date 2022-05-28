from datetime import datetime

from frenchbee import FrenchBee, Flight, PassengerInfo, Trip, DateAndLocation
from frenchbee.models import Location


def main() -> None:
    import argparse
    from pprint import pprint

    parser = argparse.ArgumentParser(description="Get French Bee airline prices.")
    parser.add_argument("origin", help="Origin airport.")
    parser.add_argument("destination", help="Destination airport.")
    parser.add_argument(
        "departure_date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        default=None,
        help="Departure date from origin airport. YYYY-mm-dd",
    )
    parser.add_argument(
        "return_date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        default=None,
        help="Return date from destination airport. YYYY-mm-dd",
    )
    parser.add_argument(
        "--passengers",
        type=int,
        default=1,
        help="Number of adult passengers. default=1",
    )
    parser.add_argument(
        "--children", type=int, default=0, help="Number of child passengers. default=0"
    )

    args = parser.parse_args()

    trip: Trip = Trip(
        origin_depart=DateAndLocation(
            date=args.departure_date, location=Location(args.origin)
        ),
        destination_return=DateAndLocation(
            date=args.return_date, location=Location(args.destination)
        ),
        passengers=PassengerInfo(Adults=args.passengers, Children=args.children),
    )

    client: FrenchBee = FrenchBee()
    departure_info: Flight = client.get_departure_info_for(trip)
    if departure_info:
        print(departure_info.json())
        return_info: Flight = client.get_return_info_for(trip)
        if return_info:
            print(return_info.json())
            print(
                f"Total price: ${departure_info.price + return_info.price} "
                + f"for {departure_info.day} to {return_info.day} "
                + f"from {departure_info.departure_airport} to {return_info.departure_airport}"
            )

            trip = client.get_flight_times(trip)
            pprint(trip.json())


if __name__ == "__main__":
    main()
