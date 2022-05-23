import unittest
from datetime import datetime, timedelta

from py_frenchbee.frenchbee import FrenchBee, PassengerInfo


class FrenchBeeTests(unittest.TestCase):
    def test_success(self):
        origin_date = datetime.today() + timedelta(days=60)
        return_date = origin_date + timedelta(days=7)
        passengers = PassengerInfo(Adults=1)

        client = FrenchBee()
        return_info = client.get_return_info_for(
            "EWR", "ORY", passengers, origin_date, return_date
        )
        self.assertGreater(return_info.price, 0, "Flight return price is invalid.")
