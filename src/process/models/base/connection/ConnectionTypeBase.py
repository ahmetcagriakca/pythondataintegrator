from typing import List
from models.base.connection.ConnectionBase import ConnectionBase
from models.base.connection.ConnectorTypeBase import ConnectorTypeBase
from models.base.EntityBase import EntityBase
from infrastructor.json.BaseConverter import BaseConverter


@BaseConverter.register
class ConnectionTypeBase(EntityBase):

    def __init__(self,
                 Name: int = None,
                 Connectors: List[ConnectorTypeBase] = [],
                 Connections: List[ConnectionBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Connections = Connections
        self.Connectors = Connectors
        self.Name: int = Name
