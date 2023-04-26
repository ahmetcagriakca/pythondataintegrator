from pdip.data.domain import EntityBase

from src.domain.base.connection.ConnectionWebServiceSoapBase import ConnectionWebServiceSoapBase


class ConnectionWebServiceBase(EntityBase):

    def __init__(self,
                 ConnectionId: int = None,
                 ConnectorTypeId: int = None,
                 Ssl: bool = None,
                 Soap: ConnectionWebServiceSoapBase = None,
                 Connection=None,
                 ConnectorType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ConnectionId: str = ConnectionId
        self.ConnectorTypeId: str = ConnectorTypeId
        self.Ssl: bool = Ssl
        self.Soap = Soap
        self.Connection = Connection
        self.ConnectorType = ConnectorType
