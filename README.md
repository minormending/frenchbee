# French Bee
Python client for finding French Bee airline prices.

# Usage
```
usage: frenchbee.py [-h] [--passengers PASSENGERS] [--children CHILDREN] origin departure_date destination return_date

Get French Bee airline prices.

positional arguments:
  origin                Origin airport.
  departure_date        Departure date from origin airport. YYYY-mm-dd
  destination           Destination airport.
  return_date           Return date from destination airport. YYYY-mm-dd

optional arguments:
  -h, --help            show this help message and exit
  --passengers PASSENGERS
                        Number of adult passengers. default=1
  --children CHILDREN   Number of child passengers. default=0
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