from __future__ import print_function

import unittest

from thepay.config import Config
from thepay.dataApi import DataApi
from thepay.payment import Payment, ReturnPayment
from six.moves import urllib

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
        self.dataApi.getPaymentInstructions(1)

    def test_credentials(self):
        self.config.setCredentials(42, 43, 'test', 'test2')

        self.assertEqual(self.config.merchantId, 42)
        self.assertEqual(self.config.accountId, 43)
        self.assertEqual(self.config.password, 'test')
        self.assertEqual(self.config.dataApiPassword, 'test2')


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

        self.assertDictEqual(dict(self.payment.getParams()),
                             {
                                 'value': 123.,
                                 'accountId': 1,
                                 'merchantId': 1,
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
                         'https://www.thepay.cz/demo-gate/?merchantId=1&accountId=1&value=123.0&description=Order+123+payment&merchantData=Order+123&customerEmail=test%40test.te&returnUrl=http%3A%2F%2Ftest.te&methodId=1&signature=7450a2ca57f4a380ed7c4e71d6e0e6bf')


class ReturnPaymentTests(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.payment = ReturnPayment(self.config)

    def test_data(self):
        params_str = 'merchantId=1&accountId=1&value=123.00&currency=CZK&methodId=1&description=Order+123+payment&merchantData=Order+123&status=2&paymentId=34886&ipRating=&isOffline=0&needConfirm=0&signature=f38ff15cc17752a6d4035044a93deb06'
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

        self.assertEqual(self.payment.getSignature(), 'f38ff15cc17752a6d4035044a93deb06')
        self.assertEqual(self.payment.getValue(), 123.0)
        self.assertEqual(self.payment.getMethodId(), 1)
        self.assertEqual(self.payment.getDescription(), 'Order 123 payment')
        self.assertEqual(self.payment.getStatus(), 2)

    def test_missing_data(self):
        self.assertRaises(ReturnPayment.MissingParameter, lambda: self.payment.parseData({}))

