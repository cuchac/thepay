import unittest
from thepay.config import Config
from thepay.dataApi import DataApi


class DataApiTests(unittest.TestCase):

    def setUp(self):
        super(DataApiTests, self).setUp()
        self.config = Config()
        self.dataApi = DataApi(self.config)

    def test_connect(self):
        self.dataApi.connect()
        methods = self.dataApi.getPaymentMethods()

        print methods[0].name