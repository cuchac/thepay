class Config(object):

    # ThePay API
    gateUrl = 'https://www.thepay.cz/demo-gate/'
    merchantId = 1
    accountId = 1
    password = 'my$up3rsecr3tp4$$word'

    # Data API
    dataApiPassword = 'my$up3rsecr3tp4$$word'
    webServicesWsdl = 'https://www.thepay.cz/demo-gate/api/api-demo.wsdl'
    dataWebServicesWsdl = 'https://www.thepay.cz/demo-gate/api/data-demo.wsdl'

    def setCredentials(self, merchantId, accountId, password, dataApiPassword=None):
        """ Set credentials for production server

        :param merchantId:
        :param accountId:
        :param password:
        :param dataApiPassword:
        """
        self.gateUrl = 'https://www.thepay.cz/gate/'
        self.webServicesWsdl = 'https://www.thepay.cz/gate/api/api.wsdl'
        self.dataWebServicesWsdl = 'https://www.thepay.cz/gate/api/data.wsdl'
        self.merchantId = merchantId
        self.accountId = accountId
        self.password = password
        self.dataApiPassword = dataApiPassword

