from __future__ import print_function

import unittest
import uuid

from thepay.config import Config
from thepay.gateApi import GateApi, GateError


class GateApiTests(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.gateApi = GateApi(self.config)

    def test_invalid_cardCreateRecurrentPayment(self):
        with self.assertRaises(GateError):
            self.gateApi.cardCreateRecurrentPayment(
                '4394c54e-27f1-411b-b5e0-3f4e1ecf3e2c',
                uuid.uuid4(),
                10
            )

    def test_cardCreateRecurrentPayment(self):
        self.gateApi.cardCreateRecurrentPayment(
            'c53be2ae-0b84-46e2-90f9-03c144a1a328',
            uuid.uuid4(),
            10
        )
