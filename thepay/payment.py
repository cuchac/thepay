from collections import OrderedDict
import hashlib
from six.moves import urllib
from thepay.utils import SignatureMixin


class Payment(SignatureMixin):
    """
    Class representing single Payment

    Payment parameters:
        value: Float value indicating the amount of money that should be paid
        currency: Currency identifier. Not used so far, reserved for future use
        description: Payment description that should be visible to the customer
        merchantData: Any merchant-specific data, that will be returned to the site after the payment has been completed
        returnUrl: URL where to redirect the user after the payment has been completed. It defaults to value configured 
                in administration interface, but can be overwritten using this property
        methodId: ID of payment method to use for paying. Setting this argument should be result of user's selection, 
                not merchant's selection
        customerData: Optional data about customer. Required for FerBuy method
        customerEmail: Customers e-mail address. Used to send payment info and payment link from the payment info page
        deposit: If card payment will be charged immediately or only blocked and charged later by paymentDeposit 
                operation 
        isRecurring: If card payment is recurring
        merchantSpecificSymbol: specific symbol (used only if payment method supports it)
    """

    def __init__(self, config):
        self.config = config
        self.data = OrderedDict((
            ('value', None),
            ('currency', None),
            ('description', None),
            ('merchantData', None),
            ('customerData', None),
            ('customerEmail', None),
            ('returnUrl', None),
            ('methodId', None),
            ('deposit', None),
            ('isRecurring', None),
            ('merchantSpecificSymbol', None),
        ))

    def setValue(self, value):
        """
        Sets the value property.
        """
        # Only positive numbers allowed.
        value = float(value)

        if value < 0:
            raise ValueError('Negative value')

        self.data['value'] = value

    def setCurrency(self, currency):
        """
        Sets the currency property.
        """
        self.data['currency'] = currency

    def setDescription(self, description):
        """
        Sets the description property.
        """
        self.data['description'] = description

    def setMerchantData(self, data):
        """
        Sets the merchantData property.
        """
        self.data['merchantData'] = data

    def setReturnUrl(self, returnUrl):
        """
        Sets the returnUrl property.
        """
        self.data['returnUrl'] = returnUrl

    def setMethodId(self, methodId):
        """
        Sets the methodId property.
        """
        self.data['methodId'] = methodId

    def getValue(self):
        """
        Returns the value property. If value was not specified using
        setValue() method, None is returned.
        """
        return self.data['value']

    def getCurrency(self):
        """
        Returns the currency property. If currency was not specified using
        setCurrency() method, None is returned.
        """
        return self.data['currency']

    def getDescription(self):
        """
        Returns the description property. If description was not specified
        using setDescription() method, None is returned.
        """
        return self.data['description']

    def getMerchantData(self):
        """
        Returns the merchantData property. If merchantData was not specified
        using setMerchantData() method, None is returned.
        """
        return self.data['merchantData']

    def getReturnUrl(self):
        """
        Returns the returnUrl property. If returnUrl was not specified using
        setReturnUrl() method, None is returned.
        """
        return self.data['returnUrl']

    def getMethodId(self):
        """
        Returns the methodId property. If methodId was not specified using
        setMethodId() property, None is returned.
        """
        return self.data['methodId']

    def setCustomerData(self, data):
        """
        Set customer data.
        @param mixed data
        """
        self.data['customerData'] = data

    def getCustomerData(self):
        """
        Get previously set customer data
        @return mixed
        """
        return self.data['customerData']

    def setCustomerEmail(self, customerEmail):
        """
        @param customerEmail None|string customerEmail
        """
        self.data['customerEmail'] = customerEmail

    def getCustomerEmail(self):
        """
        @return None|string
        """
        return self.data['customerEmail']

    def getDeposit(self):
        """
         If card payment will be charged immediately or only blocked and charged later by paymentDeposit operation.
        @return boolean
        """
        return self.data['deposit']

    def setDeposit(self, deposit):
        """
        Set if card payment will be charged immediately or only blocked and charged later by paymentDeposit operation.
        @param deposit boolean deposit
        """
        self.data['deposit'] = deposit

    def getIsRecurring(self):
        """
        If card payment is recurring.
        @return boolean
        """
        return self.data['isRecurring']

    def setIsRecurring(self, isRecurring):
        """
        Set if card payment is recurring.
        @param isRecurring boolean isRecurring
        """
        self.data['isRecurring'] = isRecurring

    def getMerchantSpecificSymbol(self):
        """
        Numerical specific symbol (used only if payment method supports it).
        @return string
        """
        return self.data['merchantSpecificSymbol']

    def setMerchantSpecificSymbol(self, merchantSpecificSymbol):
        """
        Numerical specific symbol (used only if payment method supports it).
        @return string
        """
        self.data['merchantSpecificSymbol'] = merchantSpecificSymbol

    def getParams(self):
        """
        List arguments to put into the URL. Returns associative array of
        arguments that should be contained in the ThePay gate call.
        """
        params = OrderedDict()

        params["merchantId"] = self.config.merchantId
        params["accountId"] = self.config.accountId

        for key, value in self.data.items():
            if value is not None:
                params[key] = value

        return params

    def _hashParam(self, params):
        # this interface is using deprecated md5 hashing
        return hashlib.md5(params).hexdigest()

    def getCreateUrl(self):
        """
        Returns absolute url that creates this payment

        :return: url-encoded string
        """
        params = self._signParams(self.getParams(), self.config.password)
        return "{}?{}".format(self.config.gateUrl, urllib.parse.urlencode(params))


class ReturnPayment(SignatureMixin):
    required_data = (
        "value", "currency", "methodId", "description", "merchantData",
        "status", "paymentId", "ipRating", "isOffline", "needConfirm"
    )

    optional_data = (
        "isConfirm", "variableSymbol", "specificSymbol",
        "deposit", "isRecurring", "customerAccountNumber",
        "customerAccountName"
    )

    class MissingParameter(ValueError):
        pass

    class InvalidSignature(ValueError):
        pass

    def __init__(self, config):
        self.config = config
        self.data = OrderedDict()
        self.signature = None

    def parseData(self, data):
        for key in self.required_data:
            if key not in data:
                raise self.MissingParameter(key)

            self.data[key] = data[key]

        for key in self.optional_data:
            if key not in data:
                self.data[key] = None
            else:
                self.data[key] = data[key]

        self.signature = data.get('signature', None)

    def _hashParam(self, params):
        # this interface is using deprecated md5 hashing
        return hashlib.md5(params).hexdigest()

    def checkSignature(self):
        params = OrderedDict()

        params["merchantId"] = self.config.merchantId
        params["accountId"] = self.config.accountId

        for key, value in self.data.items():
            if value is None:
                continue

            params[key] = value

        signed_params = self._signParams(params, self.config.password)

        if self.signature != signed_params['signature']:
            raise self.InvalidSignature()

        return True

    def getValue(self):
        """
        Returns the value property. If value was not specified using
        setValue() method, None is returned.
        """
        return float(self.data['value'])

    def getDescription(self):
        """
        Returns the description property. If description was not specified
        using setDescription() method, None is returned.
        """
        return self.data['description']

    def getMerchantData(self):
        """
        Returns the merchantData property. If merchantData was not specified
        using setMerchantData() method, None is returned.
        """
        return self.data['merchantData']

    def getMethodId(self):
        """
        Returns the methodId property. If methodId was not specified using
        setMethodId() property, None is returned.
        """
        return int(self.data['methodId'])

    def getCurrency(self):
        """
        Overridden to provide default value if no currency is specified in
        the callback, so that merchant application can count with different
        currencies right now, even when ThePay does not support multiple
        currencies so far.
        """
        if self.data.get('currency', None) is None:
            return "CZK"

        return self.data['currency']

    def getSignature(self):
        """
        Overwrites getSignature() method from TpPayment to return the valid
        signature specified by ThePay gate, not the signature computed
        by the class for sending the payment (mainly because sent payment
        does not contain all fields that are used to generate returned
        payment signature).
        """
        return self.signature

    def getStatus(self):
        """
        Gets status of the payment.
        @return int one of STATUS_* constants.
        """
        return int(self.data['status'])

    def getPaymentId(self):
        """
        Gets unique ID of the payment in the ThePay system.
        """
        return self.data['paymentId']

    def getIpRating(self):
        """
        Returns the IP rating of the IP that sent the payment.
        """
        return self.data['ipRating']

    def getVariableSymbol(self):
        """
        Returns the variable symbol, if valid, for offline payment method.
        """
        return self.data['variableSymbol']

    def isOfline(self):
        """
        @return boolean true if payment method is offline
        """
        return self.data['isOffline']

    def getNeedConfirm(self):
        """
        @return boolean if payment needs additional confirmation about it's state - for online methods with additional confirmation
        """
        return self.data['needConfirm']

    def getIsConfirm(self):
        """
        @return boolean if actual action is confirmation about payment state - for online methods with additional confirmation
        """
        return self.data['isConfirm']

    def getSpecificSymbol(self):
        """
        @return string specific symbol from bank transaction. Used only for permanent payments.
        """
        return self.data['specificSymbol']

    def getIsOffline(self):
        """
        @return if payment method is offline or online
        """
        return self.data['isOffline']

    def getDeposit(self):
        """
        @return boolean  If card payment will be charged immediately or only blocked and charged later by paymentDeposit operation.
        """
        return self.data['deposit']

    def getIsRecurring(self):
        """
        @return boolean If card payment is reccuring.
        """
        return self.data['isRecurring']

    def getCustomerAccountNumber(self):
        """
        @return string Number of customer's account in full format including bank code.
        """
        return self.data['customerAccountNumber']

    def getCustomerAccountName(self):
        """
        @return string Name of customer's account.
        """
        return self.data['customerAccountName']
