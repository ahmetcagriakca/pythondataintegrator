from models.base.connection import ConnectionQueueBase
from models.base.connection.ConnectionServerBase import ConnectionServerBase
from models.base.connection.ConnectionSecretBase import ConnectionSecretBase
from models.base.connection.ConnectionDatabaseBase import ConnectionDatabaseBase
from models.base.connection.ConnectionFileBase import ConnectionFileBase
from typing import List
from models.base.EntityBase import EntityBase
from models.base.integration.DataIntegrationConnectionBase import DataIntegrationConnectionBase
from infrastructor.json.BaseConverter import BaseConverter


@BaseConverter.register
class ConnectionBase(EntityBase):

    def __init__(self,
                 Name: str = None,
                 ConnectionTypeId: int = None,
                 ConnectionType=None,
                 Database: ConnectionDatabaseBase=None,
                 File: ConnectionFileBase=None,
                 Queue: ConnectionQueueBase=None,
                 ConnectionSecrets: List[ConnectionSecretBase]=[],
                 ConnectionServers: List[ConnectionServerBase]=[],
                 DataIntegrationConnections: List[DataIntegrationConnectionBase]=[],
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
