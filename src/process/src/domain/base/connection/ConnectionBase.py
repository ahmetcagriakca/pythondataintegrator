from typing import List

from pdip.data.domain import EntityBase

from src.domain.base.connection import ConnectionQueueBase
from src.domain.base.connection.ConnectionBigDataBase import ConnectionBigDataBase
from src.domain.base.connection.ConnectionDatabaseBase import ConnectionDatabaseBase
from src.domain.base.connection.ConnectionFileBase import ConnectionFileBase
from src.domain.base.connection.ConnectionSecretBase import ConnectionSecretBase
from src.domain.base.connection.ConnectionServerBase import ConnectionServerBase
from src.domain.base.integration.DataIntegrationConnectionBase import DataIntegrationConnectionBase


class ConnectionBase(EntityBase):

    def __init__(self,
                 Name: str = None,
                 ConnectionTypeId: int = None,
                 ConnectionType=None,
                 Database: ConnectionDatabaseBase = None,
                 BigData: ConnectionBigDataBase = None,
                 File: ConnectionFileBase = None,
                 Queue: ConnectionQueueBase = None,
                 ConnectionSecrets: List[ConnectionSecretBase] = [],
                 ConnectionServers: List[ConnectionServerBase] = [],
                 DataIntegrationConnections: List[DataIntegrationConnectionBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataIntegrationConnections = DataIntegrationConnections
        self.ConnectionServers = ConnectionServers
        self.ConnectionSecrets = ConnectionSecrets
        self.Database = Database
        self.File = File
        self.Queue = Queue
        self.BigData = BigData
        self.Name: str = Name
        self.ConnectionTypeId: int = ConnectionTypeId
        self.ConnectionType = ConnectionType
