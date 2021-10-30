from typing import List

from pdip.data import EntityBase

from pdi.domain.base.connection import ConnectionQueueBase
from pdi.domain.base.connection.ConnectionDatabaseBase import ConnectionDatabaseBase
from pdi.domain.base.connection.ConnectionFileBase import ConnectionFileBase
from pdi.domain.base.connection.ConnectionSecretBase import ConnectionSecretBase
from pdi.domain.base.connection.ConnectionServerBase import ConnectionServerBase
from pdi.domain.base.integration.DataIntegrationConnectionBase import DataIntegrationConnectionBase


class ConnectionBase(EntityBase):

    def __init__(self,
                 Name: str = None,
                 ConnectionTypeId: int = None,
                 ConnectionType=None,
                 Database: ConnectionDatabaseBase = None,
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
        self.Queue = Queue
        self.File = File
        self.Database = Database
        self.Name: str = Name
        self.ConnectionTypeId: int = ConnectionTypeId
        self.ConnectionType = ConnectionType
