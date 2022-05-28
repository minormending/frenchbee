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

### CLI Example
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
{'arrival_airport': 'ORY', 'currency': 'USD', 'day': '2022-10-06', 'departure_airport': 'EWR', 'is_offer': False, 'price': 264, 'tax': '117.30', 'total': 380.6}
```

## OTher

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

# Example
```
>>> python frenchbee.py EWR 2022-10-06 ORY 2022-10-10

Flight(arrival_airport='ORY', currency='USD', day='2022-10-06', departure_airport='EWR', is_offer=False, price=164, tax='99.80', total=263.6)
Flight(arrival_airport='EWR', currency='USD', day='2022-10-10', departure_airport='ORY', is_offer=False, price=270, tax='170.97', total=440.94000000000005)
Total price: $434 for 2022-10-06 to 2022-10-10 from EWR to ORY
```

# Docker

```
>>> docker build -t frenchbee .
>>> docker run frenchbee EWR 2022-10-06 ORY 2022-10-10

Flight(arrival_airport='ORY', currency='USD', day='2022-10-06', departure_airport='EWR', is_offer=False, price=164, tax='99.80', total=263.6)
Flight(arrival_airport='EWR', currency='USD', day='2022-10-10', departure_airport='ORY', is_offer=False, price=270, tax='170.97', total=440.94000000000005)
Total price: $434 for 2022-10-06 to 2022-10-10 from EWR to ORY
```