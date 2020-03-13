from __future__ import print_function

import unittest

from thepay.config import Config
from thepay.payment import Payment, ReturnPayment
from six.moves import urllib


class PaymentTests(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.payment = Payment(self.config)

    def fill_payment(self):
        self.payment.setValue(123)
        self.payment.setReturnUrl('http://test.te')
        self.payment.setCustomerEmail('test@test.te')
        self.payment.setDescription('Order 123 payment')
        self.payment.setMethodId(1)
        self.payment.setMerchantData('Order 123')

    def test_data(self):
        self.fill_payment()

        self.assertEqual(self.payment.getValue(), 123)
        self.assertEqual(self.payment.getReturnUrl(), 'http://test.te')
        self.assertEqual(self.payment.getCustomerEmail(), 'test@test.te')
        self.assertEqual(self.payment.getDescription(), 'Order 123 payment')
        self.assertEqual(self.payment.getMethodId(), 1)
        self.assertEqual(self.payment.getMerchantData(), 'Order 123')

    def test_wrong_data(self):
        self.assertRaises(ValueError, lambda: self.payment.setValue('-120'))

    def test_params(self):
        self.fill_payment()

        self.assertDictEqual(dict(self.payment._getParams()),
                             {
                                 'value': 123.,
                                 'accountId': self.config.accountId,
                                 'merchantId': self.config.merchantId,
                                 'returnUrl': 'http://test.te',
                                 'customerEmail': 'test@test.te',
                                 'description': 'Order 123 payment',
                                 'methodId': 1,
                                 'merchantData': 'Order 123',
                             })

        self.payment.setCurrency('USD')
        self.assertEqual(self.payment.getCurrency(), 'USD')

        self.payment.setCustomerData('test')
        self.assertEqual(self.payment.getCustomerData(), 'test')

        self.payment.setDeposit(321)
        self.assertEqual(self.payment.getDeposit(), 321)

        self.payment.setIsRecurring(True)
        self.assertEqual(self.payment.getIsRecurring(), True)

    def test_url(self):
        self.fill_payment()
        self.assertEqual(self.payment.getCreateUrl(),
            "https://www.thepay.cz/demo-gate/?merchantId=1&accountId=3&value=123.0&description=Order+123+payment&merchantData=Order+123&customerEmail=test%40test.te&returnUrl=http%3A%2F%2Ftest.te&methodId=1&signature=9edd1af378d8168f5023d03831d18a52"
        )


class ReturnPaymentTests(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.payment = ReturnPayment(self.config)

    def test_data(self):
        params_str = 'merchantId=1&accountId=3&value=123.00&currency=CZK&methodId=1&description=Order+123+payment&merchantData=Order+123&status=2&paymentId=1006482871&ipRating=&isOffline=0&needConfirm=0&signature=45711869e9fc739d1c0e7d98b223a279'
        params = urllib.parse.parse_qs(params_str, keep_blank_values=True)
        params = {key: value[0] for key, value in params.items()}

        self.payment.parseData(params)

        self.payment.checkSignature()

        self.assertIsNotNone(self.payment.getPaymentId())

        self.assertEqual(self.payment.getCurrency(), 'CZK')

        params['isConfirm'] = '1'
        params['currency'] = None
        self.payment.parseData(params)
        self.assertEqual(self.payment.getCurrency(), 'CZK')
        self.assertRaises(ReturnPayment.InvalidSignature, lambda: self.payment.checkSignature())

        self.assertEqual(self.payment.getSignature(), '45711869e9fc739d1c0e7d98b223a279')
        self.assertEqual(self.payment.getValue(), 123.0)
        self.assertEqual(self.payment.getMethodId(), 1)
        self.assertEqual(self.payment.getDescription(), 'Order 123 payment')
        self.assertEqual(self.payment.getStatus(), 2)

    def test_missing_data(self):
        self.assertRaises(ReturnPayment.MissingParameter, lambda: self.payment.parseData({}))
