# French Bee
Python client for finding French Bee airline prices.

# Usage
```
usage: frenchbee-cli [-h] {data,flight} ...

Get French Bee airline prices.

positional arguments:
  {data,flight}
    data         Get metadata about French Bee.
    flight       Get flight information.

options:
  -h, --help     show this help message and exit
```

```
> frenchbee-cli data --help     
usage: frenchbee-cli data [-h] [--locations]

options:
  -h, --help   show this help message and exit
  --locations  Get all supported locations.

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