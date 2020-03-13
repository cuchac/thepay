from collections import OrderedDict
import hashlib

from suds.client import Client

from six.moves.urllib.parse import urlencode

from thepay.utils import SignatureMixin


class GateError(Exception):
    pass


class GateApi(SignatureMixin):
    def __init__(self, config):
        """

        :param config: Config
        """
        self.config = config
        self.client = None

        self.connect()

    def connect(self):
        self.client = Client(self.config.webServicesWsdl)

    def _hashParam(self, params):
        # this interface is using deprecated md5 hashing
        return hashlib.md5(params).hexdigest()

    def _buildQuery(self, params):
        # this interface uses different way of encoding
        return urlencode(params)

    def cardCreateRecurrentPayment(self, merchantData, newMerchantData, value):
        params = self._signParams(OrderedDict((
            ('merchantId', self.config.merchantId),
            ('accountId', self.config.accountId),
            ('merchantData', merchantData),
            ('newMerchantData', newMerchantData),
            ('value', value),
        )), self.config.password)
        response = self.client.service.cardCreateRecurrentPaymentRequest(**params)
        if not response.status:
            raise GateError(response.errorDescription)
