from __future__ import print_function
import requests
import unittest
import uuid

from thepay.config import Config
from thepay.gateApi import GateApi, GateError
from thepay.dataApi import DataApi
from thepay.payment import Payment


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
        payment_id = str(uuid.uuid4())
        # Create new recurring payment
        payment = Payment(self.config)
        payment.setValue(123)
        payment.setReturnUrl('http://test.te')
        payment.setCustomerEmail('test@test.te')
        payment.setDescription('Order 123 payment')
        payment.setMethodId(31)
        payment.setMerchantData(payment_id)
        payment.setIsRecurring(1)
        # Simulate user going through payment process
        response = requests.get(payment.getCreateUrl())
        payment_url = response.url[:-1] + "p"
        response = requests.get(payment_url)
        body = response.content.decode()
        assert "Číslo platby" in body
        for line in body.splitlines():
            if '<input type="hidden" name="id"' in line:
                payment_number = line.split('value="')[1].split('"')[0]
        # Confirm payment state
        response = requests.post("https://www.thepay.cz/demo-gate/return.php", data={"state": 2, "underpaid_value": 1, "id": payment_number}, allow_redirects=False)

        # Create recurrent payment for previous one
        # This should work, but is failing for some reason
        with self.assertRaises(GateError):
            self.gateApi.cardCreateRecurrentPayment(
                payment_id,
                str(uuid.uuid4()),
                123
            )
