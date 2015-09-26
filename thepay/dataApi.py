from collections import OrderedDict
import suds.client

from thepay.utils import SignatureMixin


class DataApi(SignatureMixin):
    def __init__(self, config):
        """

        :param config: Config
        """
        self.config = config
        self.client = None

        self.connect()

    def connect(self):
        self.client = suds.client.Client(self.config.dataWebServicesWsdl)

    def getPaymentMethods(self):
        params = self._signParams(OrderedDict((
            ('merchantId', self.config.merchantId),
            ('accountId', self.config.accountId),
        )), self.config.dataApiPassword)
        return self.client.service.getPaymentMethods(**params).methods[0]

    def getPaymentState(self, paymentId):
        params = self._signParams(OrderedDict((
            ('merchantId', self.config.merchantId),
            ('paymentId', paymentId),
        )), self.config.dataApiPassword)
        return int(self.client.service.getPaymentState(**params).state)

    def getPayment(self, paymentId):
        params = self._signParams(OrderedDict((
            ('merchantId', self.config.merchantId),
            ('paymentId', paymentId),
        )), self.config.dataApiPassword)
        return self.client.service.getPayment(**params).payment

    def getPaymentInstructions(self, paymentId):
        params = self._signParams(OrderedDict((
            ('merchantId', self.config.merchantId),
            ('paymentId', paymentId),
        )), self.config.dataApiPassword)
        return self.client.service.getPaymentInstructions(**params).paymentInfo
