from pdip.data.domain import EntityBase



class ConnectionWebServiceSoapBase(EntityBase):
    def __init__(self,
                 ConnectionWebServiceId: int = None,
                 Wsdl: str = None,
                 ConnectionWebService = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ConnectionWebServiceId: int = ConnectionWebServiceId
        self.Wsdl: str = Wsdl
        self.ConnectionWebService = ConnectionWebService
