# French Bee
Python client for finding French Bee airline prices.

# Installation
``
pip install frenchbee
``

# Usage
The [FrenchBeeData](frenchbee/data.py) class is used for looking up travel location codes that French Bee airlines supports. Note that locations include airports and train stations. Available methods are:
- [get_locations()](#get-locations): Get all the supported airport and train stations.

The [FrenchBee](frenchbee/frenchbee.py) class is used for looking up flight prices and times. Available methods are:
- [get_departure_info_for(...)](#get-departure-info): Get pricing info for a specific departure day between two locations.
- [get_departure_availability(...)](#get-departure-availability): Get pricing info between two locations for the next few months.
- [get_return_info_for(...)](#get-return-info): Get pricing info for a specific departure and return day between two locations.
- [get_return_availability(...)](#get-return-availability): Get return pricing info for a specific departure day between two locations for the next few months.
- [get_flight_times(...)](#get-flight-times): Get flight times info for a specific departure and return day between two locations.

## Get Locations
Get all the French Bee supported airport and train stations.

### Example
```
from frenchbee import FrenchBeeData, Location

client: FrenchBeeData = FrenchBeeData()
locations: List[Location] = list(client.get_locations())
for location in locations:
  print(location.json())
```

### Results
```
{'code': 'PUJ', 'name': 'Punta Cana, Dominican Republic'}
{'code': 'QXB', 'name': 'Aix-en-provence TGV (Railway Station), France '}
{'code': 'QXG', 'name': 'Angers St-Laud TGV (Railway Station), France '}
```

## Get Departure Info
Get pricing info for a specific departure day between two locations.

### Example
```
from datetime import datetime
from frenchbee import FrenchBee
from frenchbee import Trip, PassengerInfo, DateAndLocation, Location, Flight

trip: Trip = Trip(
  origin_depart=DateAndLocation(
    date=datetime(2022, 10, 6), location=Location("EWR")
  ),
  destination_return=DateAndLocation(
    date=None, location=Location("ORY")
  ),
  passengers=PassengerInfo(Adults=1),
)

client: FrenchBee = FrenchBee()
flight: Flight = client.get_departure_info_for(trip)
print(flight.json())
```

### Results
```
{'arrival_airport': 'ORY', 'currency': 'USD', 'day': '2022-10-06', 'departure_airport': 'EWR', 'is_offer': False, 'price': 264.0, 'tax': 117.3}
```

## Get Departure Availability
Get pricing info between two locations for the next few months.

### Example
```
from datetime import datetime
from frenchbee import FrenchBee
from frenchbee import Trip, PassengerInfo, DateAndLocation, Location, Flight

trip: Trip = Trip(
  origin_depart=DateAndLocation(
    date=None, location=Location("EWR")
  ),
  destination_return=DateAndLocation(
    date=None, location=Location("ORY")
  ),
  passengers=PassengerInfo(Adults=1),
)

client: FrenchBee = FrenchBee()
flights: Dict[datetime, Flight] = client.get_departure_availability(trip)
for date, flight in flights.items():
  print(date, flight.json())
```

### Results
```
2022-05-28 00:00:00 {'arrival_airport': 'ORY', 'currency': 'USD', 'day': '2022-05-28', 'departure_airport': 'EWR', 'is_offer': False, 'price': 1115.0, 'tax': 117.3}
2022-05-29 00:00:00 {'arrival_airport': 'ORY', 'currency': 'USD', 'day': '2022-05-29', 'departure_airport': 'EWR', 'is_offer': True, 'price': 1015.0, 'tax': 117.3}
2022-05-30 00:00:00 {'arrival_airport': 'ORY', 'currency': 'USD', 'day': '2022-05-30', 'departure_airport': 'EWR', 'is_offer': True, 'price': 1015.0, 'tax': 117.3}
```




## Get Return Info
Get pricing info for a specific departure and return day between two locations.

### Example
```
from datetime import datetime
from frenchbee import FrenchBee
from frenchbee import Trip, PassengerInfo, DateAndLocation, Location, Flight

trip: Trip = Trip(
  origin_depart=DateAndLocation(
    date=datetime(2022, 10, 6), location=Location("EWR")
  ),
  destination_return=DateAndLocation(
    date=datetime(2022, 10, 10), location=Location("ORY")
  ),
  passengers=PassengerInfo(Adults=1),
)

client: FrenchBee = FrenchBee()
flight: Flight = client.get_return_info_for(trip)
print(flight.json())
```

### Results
```
{'arrival_airport': 'EWR', 'currency': 'USD', 'day': '2022-10-10', 'departure_airport': 'ORY', 'is_offer': False, 'price': 332.0, 'tax': 186.47}
```

## Get Return Availability
Get return pricing info for a specific departure day between two locations for the next few months.

### Example
```
from datetime import datetime
from frenchbee import FrenchBee
from frenchbee import Trip, PassengerInfo, DateAndLocation, Location, Flight

trip: Trip = Trip(
  origin_depart=DateAndLocation(
    date=datetime(2022, 10, 6), location=Location("EWR")
  ),
  destination_return=DateAndLocation(
    date=None, location=Location("ORY")
  ),
  passengers=PassengerInfo(Adults=1),
)

client: FrenchBee = FrenchBee()
flights: Dict[datetime, Flight] = client.get_return_availability(trip)
for date, flight in flights.items():
  print(date, flight.json())
```

### Results
```
2022-10-07 00:00:00 {'arrival_airport': 'EWR', 'currency': 'USD', 'day': '2022-10-07', 'departure_airport': 'ORY', 'is_offer': False, 'price': 332.0, 'tax': 186.47}
2022-10-08 00:00:00 {'arrival_airport': 'EWR', 'currency': 'USD', 'day': '2022-10-08', 'departure_airport': 'ORY', 'is_offer': False, 'price': 332.0, 'tax': 186.47}
2022-10-09 00:00:00 {'arrival_airport': 'EWR', 'currency': 'USD', 'day': '2022-10-09', 'departure_airport': 'ORY', 'is_offer': False, 'price': 332.0, 'tax': 186.47}
```




## Get Flight Times
Get flight times info for a specific departure and return day between two locations.

### Example
```
from datetime import datetime
from frenchbee import FrenchBee
from frenchbee import Trip, PassengerInfo, DateAndLocation, Location, Flight

trip: Trip = Trip(
  origin_depart=DateAndLocation(
    date=datetime(2022, 10, 6), location=Location("EWR")
  ),
  destination_return=DateAndLocation(
    date=datetime(2022, 10, 10), location=Location("ORY")
  ),
  passengers=PassengerInfo(Adults=1),
)

client: FrenchBee = FrenchBee()
trip: Trip = client.get_flight_times(trip)
print(trip.json())
```

### Results
```
{'destination_return': {'date': '2022-10-10', 'location': {'code': 'ORY'}},
 'destination_segments': [[{'airline_code': 'BF',
                            'airline_name': 'French Bee',
                            'duration': 29700000,
                            'end': {'date': '2022-10-11 01:00:00',
                                    'location': {'code': 'EWR',
                                                 'name': 'Newark Liberty '
                                                         'International',
                                                 'terminal': 'B'}},
                            'flight_num': '720',
                            'start': {'date': '2022-10-10 16:45:00',
                                      'location': {'code': 'ORY',
                                                   'name': 'Orly',
                                                   'terminal': '4',
                                                   'transport': 'Airbus '
                                                                'A350-900'}}}]],
 'origin_depart': {'date': '2022-10-06', 'location': {'code': 'EWR'}},
 'origin_segments': [[{'airline_code': 'BF',
                       'airline_name': 'French Bee',
                       'duration': 26700000,
                       'end': {'date': '2022-10-07 10:20:00',
                               'location': {'code': 'ORY',
                                            'name': 'Orly',
                                            'terminal': '4'}},
                       'flight_num': '721',
                       'start': {'date': '2022-10-07 02:55:00',
                                 'location': {'code': 'EWR',
                                              'name': 'Newark Liberty '
                                                      'International',
                                              'terminal': 'B',
                                              'transport': 'Airbus '
                                                           'A350-900'}}}]],
 'passengers': {'Adults': 1, 'Children': 0, 'Infants': 0}}
```



# CLI Usage
This package comes bundled with a CLI tool for exploring French Bee prices and times, succinctly named `frenchbee-cli` that can be installed via `poetry install`.

```
usage: frenchbee-cli [-h] {data,flight} ...

Get French Bee airline prices.

positional arguments:
  {data,flight}
    data         Get metadata about French Bee locations.
    flight       Get flight information.

options:
  -h, --help     show this help message and exit
```

## Get Locations
```
>>> frenchbee-cli data --help     
usage: frenchbee-cli data [-h] [--locations]

options:
  -h, --help   show this help message and exit
  --locations  Get all supported locations.

>>> frenchbee-cli data --locations

{'code': 'PUJ', 'name': 'Punta Cana, Dominican Republic'}
{'code': 'QXB', 'name': 'Aix-en-provence TGV (Railway Station), France '}
{'code': 'QXG', 'name': 'Angers St-Laud TGV (Railway Station), France '}
```

# Get Flight Times
```
>>> frenchbee-cli flight EWR ORY 2022-10-06 2022-10-10

{'arrival_airport': 'ORY', 'currency': 'USD', 'day': '2022-10-06', 'departure_airport': 'EWR', 'is_offer': False, 'price': 264.0, 'tax': 117.3}
{'arrival_airport': 'EWR', 'currency': 'USD', 'day': '2022-10-10', 'departure_airport': 'ORY', 'is_offer': False, 'price': 332.0, 'tax': 186.47}
Total price: $596.0 for 2022-10-06 00:00:00 to 2022-10-10 00:00:00 from EWR to ORY
{'destination_return': {'date': '2022-10-10', 'location': {'code': 'ORY'}},
 'destination_segments': [[{'airline_code': 'BF',
                            'airline_name': 'French Bee',
                            'duration': 29700000,
                            'end': {'date': '2022-10-11 01:00:00',
                                    'location': {'code': 'EWR',
                                                 'name': 'Newark Liberty '
                                                         'International',
                                                 'terminal': 'B'}},
                            'flight_num': '720',
                            'start': {'date': '2022-10-10 16:45:00',
                                      'location': {'code': 'ORY',
                                                   'name': 'Orly',
                                                   'terminal': '4',
                                                   'transport': 'Airbus '
                                                                'A350-900'}}}]],
 'origin_depart': {'date': '2022-10-06', 'location': {'code': 'EWR'}},
 'origin_segments': [[{'airline_code': 'BF',
                       'airline_name': 'French Bee',
                       'duration': 26700000,
                       'end': {'date': '2022-10-07 10:20:00',
                               'location': {'code': 'ORY',
                                            'name': 'Orly',
                                            'terminal': '4'}},
                       'flight_num': '721',
                       'start': {'date': '2022-10-07 02:55:00',
                                 'location': {'code': 'EWR',
                                              'name': 'Newark Liberty '
                                                      'International',
                                              'terminal': 'B',
                                              'transport': 'Airbus '
                                                           'A350-900'}}}]],
 'passengers': {'Adults': 1, 'Children': 0, 'Infants': 0}}
```

# Docker
Containers are automatically built off of the main branch and can be downloaded from:
https://hub.docker.com/repository/docker/minormending/frenchbee

Alternatively, you can build your own containers:
```
>>> docker build -t frenchbee .
>>> docker run frenchbee flight EWR ORY 2022-10-06 2022-10-10

{'arrival_airport': 'ORY', 'currency': 'USD', 'day': '2022-10-06', 'departure_airport': 'EWR', 'is_offer': False, 'price': 264.0, 'tax': 117.3}
{'arrival_airport': 'EWR', 'currency': 'USD', 'day': '2022-10-10', 'departure_airport': 'ORY', 'is_offer': False, 'price': 332.0, 'tax': 186.47}
Total price: $596.0 for 2022-10-06 00:00:00 to 2022-10-10 00:00:00 from EWR to ORY
{'destination_return': {'date': '2022-10-10', 'location': {'code': 'ORY'}},
 'destination_segments': [[{'airline_code': 'BF',
                            'airline_name': 'French Bee',
                            'duration': 29700000,
                            'end': {'date': '2022-10-11 01:00:00',
                                    'location': {'code': 'EWR',
                                                 'name': 'Newark Liberty '
                                                         'International',
                                                 'terminal': 'B'}},
                            'flight_num': '720',
                            'start': {'date': '2022-10-10 16:45:00',
                                      'location': {'code': 'ORY',
                                                   'name': 'Orly',
                                                   'terminal': '4',
                                                   'transport': 'Airbus '
                                                                'A350-900'}}}]],
 'origin_depart': {'date': '2022-10-06', 'location': {'code': 'EWR'}},
 'origin_segments': [[{'airline_code': 'BF',
                       'airline_name': 'French Bee',
                       'duration': 26700000,
                       'end': {'date': '2022-10-07 10:20:00',
                               'location': {'code': 'ORY',
                                            'name': 'Orly',
                                            'terminal': '4'}},
                       'flight_num': '721',
                       'start': {'date': '2022-10-07 02:55:00',
                                 'location': {'code': 'EWR',
                                              'name': 'Newark Liberty '
                                                      'International',
                                              'terminal': 'B',
                                              'transport': 'Airbus '
                                                           'A350-900'}}}]],
 'passengers': {'Adults': 1, 'Children': 0, 'Infants': 0}}
```