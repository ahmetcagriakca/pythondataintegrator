from pdip.data.domain import EntityBase


class ConnectionServerBase(EntityBase):

    def __init__(self,
                 ConnectionId: int = None,
                 Host: str = None,
                 Port: int = None,
                 Connection=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ConnectionId: str = ConnectionId
        self.Host: str = Host
        self.Port: int = Port
        self.Connection = Connection
