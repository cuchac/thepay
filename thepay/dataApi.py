from collections import OrderedDict
from datetime import timezone

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

    def getPayments(self, account_ids=None, value_from=None, value_to=None, created_on_from=None, created_on_to=None,
                    finished_on_from=None, finished_on_to=None, page=None, state_ids=None, merchant_data=None,
                    method_ids=None):

        search_params = OrderedDict()

        if account_ids is not None:
            search_params['accountId'] = account_ids

        if state_ids is not None:
            search_params['state'] = state_ids

        if value_from is not None:
            search_params['valueFrom'] = value_from

        if value_to is not None:
            search_params['valueTo'] = value_to

        if created_on_from is not None:
            search_params['createdOnFrom'] = self._format_datetime(created_on_from)

        if created_on_to is not None:
            search_params['createdOnTo'] = self._format_datetime(created_on_to)

        if finished_on_from is not None:
            search_params['finishedOnFrom'] = self._format_datetime(finished_on_from)

        if finished_on_to is not None:
            search_params['finishedOnTo'] = self._format_datetime(finished_on_to)

        if merchant_data is not None:
            search_params['merchantData'] = merchant_data

        if method_ids is not None:
            search_params['method'] = method_ids

        params = OrderedDict((
            ('merchantId', self.config.merchantId),
        ))

        if search_params:
            params['searchParams'] = search_params

        if page:
            params['pagination'] = {'page': page}
        params['ordering'] = {'orderHow': 'ASC'}

        signed_params = self._signParams(params, self.config.dataApiPassword)

        self._convert_to_soap_array(params, 'accountId')
        self._convert_to_soap_array(params, 'state')
        self._convert_to_soap_array(params, 'method')

        return self.client.service.getPayments(**signed_params)

    def _format_datetime(self, value):
        """

        :type value: datetime.datetime
        """
        if not value.tzinfo:
            value = value.replace(tzinfo=timezone.utc).astimezone()
        return value.replace(microsecond=0).isoformat()

    def _convert_to_soap_array(self, params, attribute):
        if params.get('searchParams', {}).get(attribute):
            array = self.client.factory.create('idArray')
            array.id = params['searchParams'][attribute]
            params['searchParams'][attribute] = array
