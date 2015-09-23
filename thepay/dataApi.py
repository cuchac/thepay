from collections import OrderedDict
import hashlib
import suds.client
import six


class DataApi(object):
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
        params = self._getParams(OrderedDict((
            ('merchantId', self.config.merchantId),
            ('accountId', self.config.accountId),
        )))
        return self.client.service.getPaymentMethods(**params).methods[0]

    def getPaymentState(self, paymentId):
        params = self._getParams(OrderedDict((
            ('merchantId', self.config.merchantId),
            ('paymentId', paymentId),
        )))
        return int(self.client.service.getPaymentState(**params).state)

    def getPayment(self, paymentId):
        params = self._getParams(OrderedDict((
            ('merchantId', self.config.merchantId),
            ('paymentId', paymentId),
        )))
        return self.client.service.getPayment(**params).payment

    def getPaymentInstructions(self, paymentId):
        params = self._getParams(OrderedDict((
            ('merchantId', self.config.merchantId),
            ('paymentId', paymentId),
        )))
        return self.client.service.getPaymentInstructions(**params).paymentInfo

    def _getParams(self, params):
        """

        :type params: OrderedDict
        """
        hash_params = OrderedDict(params)
        hash_params['password'] = self.config.dataApiPassword

        param_str = "&".join('='.join(map(six.text_type, pair)) for pair in hash_params.items())

        params['signature'] = hashlib.sha256(param_str.encode('utf-8')).hexdigest()

        return params
