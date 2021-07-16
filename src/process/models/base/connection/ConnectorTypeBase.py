from models.base.connection.ConnectionQueueBase import ConnectionQueueBase
from typing import List

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base.connection.ConnectionDatabaseBase import ConnectionDatabaseBase
from models.base.connection.ConnectionFileBase import ConnectionFileBase
from models.base.EntityBase import EntityBase
from infrastructure.json.BaseConverter import BaseConverter


@BaseConverter.register
class ConnectorTypeBase(EntityBase):
    def __init__(self,
                 Name: int = None,
                 ConnectionTypeId: int = None,
                 ConnectionType = None,
                 Databases: List[ConnectionDatabaseBase]=[],
                 Files: List[ConnectionFileBase] = [],
                 Queues: List[ConnectionQueueBase]=[],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Queues = Queues
        self.Files = Files
        self.Databases = Databases
        self.Name: int = Name
        self.ConnectionTypeId: int = ConnectionTypeId
        self.ConnectionType = ConnectionType
