import unittest
from thepay.config import Config
from thepay.dataApi import DataApi


class DataApiTests(unittest.TestCase):

    def setUp(self):
        super(DataApiTests, self).setUp()
        self.config = Config()
        self.dataApi = DataApi(self.config)

    def test_methods(self):
        self.assertEqual(self.dataApi.getPaymentMethods()[0].name, 'Platba kartou')

    def test_payment_statue(self):
        self.assertEqual(self.dataApi.getPaymentState(1), 2)

    def test_payment(self):
        self.assertEqual(self.dataApi.getPayment(1).id, '1')

    def test_payment_info(self):
        print self.dataApi.getPaymentInstructions(1)


