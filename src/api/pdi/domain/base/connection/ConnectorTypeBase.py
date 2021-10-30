from typing import List

from pdip.data import EntityBase

from pdi.domain.base.connection.ConnectionDatabaseBase import ConnectionDatabaseBase
from pdi.domain.base.connection.ConnectionFileBase import ConnectionFileBase
from pdi.domain.base.connection.ConnectionQueueBase import ConnectionQueueBase


class ConnectorTypeBase(EntityBase):
    def __init__(self,
                 Name: int = None,
                 ConnectionTypeId: int = None,
                 ConnectionType=None,
                 Databases: List[ConnectionDatabaseBase] = [],
                 Files: List[ConnectionFileBase] = [],
                 Queues: List[ConnectionQueueBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Queues = Queues
        self.Files = Files
        self.Databases = Databases
        self.Name: int = Name
        self.ConnectionTypeId: int = ConnectionTypeId
        self.ConnectionType = ConnectionType
