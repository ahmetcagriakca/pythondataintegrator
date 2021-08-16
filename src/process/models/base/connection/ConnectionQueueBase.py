
from models.base.EntityBase import EntityBase
from infrastructure.json.BaseConverter import BaseConverter


@BaseConverter.register
class ConnectionQueueBase(EntityBase):

    def __init__(self,
                 ConnectionId: int = None,
                 ConnectorTypeId: int = None,
                 Protocol: str = None,
                 Mechanism: str = None,
                 Connection=None,
                 ConnectorType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ConnectionId: str = ConnectionId
        self.ConnectorTypeId: str = ConnectorTypeId
        self.Protocol: str = Protocol
        self.Mechanism: str = Mechanism
        self.Connection = Connection
        self.ConnectorType = ConnectorType
