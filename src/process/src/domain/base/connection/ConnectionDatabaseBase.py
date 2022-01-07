from pdip.data.domain import EntityBase


class ConnectionDatabaseBase(EntityBase):

    def __init__(self,
                 ConnectionId: int = None,
                 ConnectorTypeId: int = None,
                 Host: str = None,
                 Port: int = None,
                 Sid: str = None,
                 ServiceName: str = None,
                 DatabaseName: str = None,
                 Connection=None,
                 ConnectorType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ConnectionId: str = ConnectionId
        self.ConnectorTypeId: str = ConnectorTypeId
        self.Host: str = Host
        self.Port: int = Port
        self.Sid: str = Sid
        self.ServiceName: str = ServiceName
        self.DatabaseName: str = DatabaseName
        self.Connection = Connection
        self.ConnectorType = ConnectorType
