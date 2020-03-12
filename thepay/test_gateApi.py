from __future__ import print_function

import unittest
import uuid

from thepay.config import Config
from thepay.gateApi import GateApi, GateError
from thepay.dataApi import DataApi


class GateApiTests(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.gateApi = GateApi(self.config)
        self.dataApi = DataApi(self.config)

    def test_invalid_cardCreateRecurrentPayment(self):
        with self.assertRaises(GateError):
            self.gateApi.cardCreateRecurrentPayment(
                '4394c54e-27f1-411b-b5e0-3f4e1ecf3e2c',
                uuid.uuid4(),
                10
            )

    def test_cardCreateRecurrentPayment(self):
        for payment in self.dataApi.getPayments(method_ids=[21, 31], state_ids=[2]).payments.payment:
            if payment.merchantData and payment.recurring and payment.deposit:
                break
        self.gateApi.cardCreateRecurrentPayment(
            payment.merchantData,
            uuid.uuid4(),
            1
        )
