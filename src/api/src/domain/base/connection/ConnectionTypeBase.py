from typing import List

from pdip.data.domain import EntityBase

from src.domain.base.connection.ConnectionBase import ConnectionBase
from src.domain.base.connection.ConnectorTypeBase import ConnectorTypeBase


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
