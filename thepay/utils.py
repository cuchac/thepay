import hashlib
import six
from collections import OrderedDict


class SignatureMixin(object):
    @staticmethod
    def _buildQuery(params):
        return "&".join('='.join(map(six.text_type, pair)) for pair in params.items())

    def _signParams(self, params, password):
        """
        Calculate signature of all @params and append to param @OrderedDict

        :type params: OrderedDict
        """
        hash_params = OrderedDict(params)
        hash_params['password'] = password

        param_str = self._buildQuery(hash_params)

        params['signature'] = self._hashParam(param_str.encode('utf-8'))

        return params

    def _hashParam(self, params):
        return hashlib.sha256(params).hexdigest()
