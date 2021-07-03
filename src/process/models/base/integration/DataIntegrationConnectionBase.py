from models.base.EntityBase import EntityBase
from models.base.integration.DataIntegrationConnectionDatabaseBase import DataIntegrationConnectionDatabaseBase
from models.base.integration.DataIntegrationConnectionFileBase import DataIntegrationConnectionFileBase
from models.base.integration.DataIntegrationConnectionQueueBase import DataIntegrationConnectionQueueBase
from infrastructor.json.BaseConverter import BaseConverter


@BaseConverter.register
class DataIntegrationConnectionBase(EntityBase):

    def __init__(self,
                 SourceOrTarget: int = None,
                 DataIntegrationId: int = None,
                 ConnectionId: int = None,
                 DataIntegration=None,
                 Connection=None,
                 Database:DataIntegrationConnectionDatabaseBase=None,
                 File:DataIntegrationConnectionFileBase=None,
                 Queue:DataIntegrationConnectionQueueBase=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SourceOrTarget: int = SourceOrTarget
        self.DataIntegrationId: str = DataIntegrationId
        self.ConnectionId: str = ConnectionId
        self.DataIntegration = DataIntegration
        self.Connection = Connection
        self.Database = Database
        self.File = File
        self.Queue = Queue
