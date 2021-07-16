
from models.base.EntityBase import EntityBase
from infrastructure.json.BaseConverter import BaseConverter


@BaseConverter.register
class ConnectionFileBase(EntityBase):

    def __init__(self,
                 ConnectionId: int = None,
                 ConnectorTypeId: int = None,
                 Connection=None,
                 ConnectorType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ConnectionId: str = ConnectionId
        self.ConnectorTypeId: str = ConnectorTypeId
        self.Connection = Connection
        self.ConnectorType = ConnectorType
