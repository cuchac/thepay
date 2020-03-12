from __future__ import print_function

import unittest
import datetime
from datetime import tzinfo, timedelta

from thepay.config import Config
from thepay.dataApi import DataApi


class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)


class DataApiTests(unittest.TestCase):
    def setUp(self):
        super(DataApiTests, self).setUp()
        self.config = Config()
        self.dataApi = DataApi(self.config)

    def test_methods(self):
        self.assertEqual(self.dataApi.getPaymentMethods()[0].name, 'Platba24')

    def test_payment_state(self):
        self.assertEqual(self.dataApi.getPaymentState(1006402161), 1)

    def test_payment(self):
        self.assertEqual(self.dataApi.getPayment(1006402161).id, '1006402161')

    def test_payment_info(self):
        self.dataApi.getPaymentInstructions(1006402161)

    def test_payments(self):
        self.dataApi.getPayments(finished_on_from=datetime.datetime.now(UTC()) - datetime.timedelta(days=1))
        self.dataApi.getPayments(state_ids=[2])

    def test_credentials(self):
        self.config.setCredentials(42, 43, 'test', 'test2')

        self.assertEqual(self.config.merchantId, 42)
        self.assertEqual(self.config.accountId, 43)
        self.assertEqual(self.config.password, 'test')
        self.assertEqual(self.config.dataApiPassword, 'test2')
