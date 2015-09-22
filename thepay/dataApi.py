from collections import OrderedDict
import hashlib
import suds.client


class DataApi(object):
    def __init__(self, config):
        """

        :param config: Config
        """
        self.config = config
        self.client = None

    def connect(self):
        self.client = suds.client.Client(self.config.dataWebServicesWsdl)

    def getPaymentMethods(self):
        params = self.getParams(OrderedDict((
            ('merchantId', self.config.merchantId),
            ('accountId', self.config.accountId),
        )))
        return self.client.service.getPaymentMethods(**params).methods[0]

    def getParams(self, params):
        """

        :type params: OrderedDict
        """
        hash_params = OrderedDict(params)
        hash_params['password'] = self.config.dataApiPassword

        param_str = "&".join('='.join(map(unicode, pair)) for pair in hash_params.items())

        params['signature'] = hashlib.sha256(param_str).hexdigest()

        return params
