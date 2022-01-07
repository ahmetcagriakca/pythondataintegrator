from pdip.data.domain import EntityBase


class ConnectionBigDataBase(EntityBase):

    def __init__(self,
                 ConnectionId: int = None,
                 ConnectorTypeId: int = None,
                 DatabaseName: str = None,
                 Ssl: bool = None,
                 UseOnlySspi: bool = None,
                 Connection=None,
                 ConnectorType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ConnectionId: str = ConnectionId
        self.ConnectorTypeId: str = ConnectorTypeId
        self.DatabaseName: str = DatabaseName
        self.Ssl: bool = Ssl
        self.UseOnlySspi: bool = UseOnlySspi
        self.Connection = Connection
        self.ConnectorType = ConnectorType
