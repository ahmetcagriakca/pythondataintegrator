from pdip.data.domain import EntityBase

from src.domain.base.integration.DataIntegrationConnectionBigDataBase import DataIntegrationConnectionBigDataBase
from src.domain.base.integration.DataIntegrationConnectionDatabaseBase import DataIntegrationConnectionDatabaseBase
from src.domain.base.integration.DataIntegrationConnectionFileBase import DataIntegrationConnectionFileBase
from src.domain.base.integration.DataIntegrationConnectionQueueBase import DataIntegrationConnectionQueueBase


class DataIntegrationConnectionBase(EntityBase):

    def __init__(self,
                 SourceOrTarget: int = None,
                 DataIntegrationId: int = None,
                 ConnectionId: int = None,
                 DataIntegration=None,
                 Connection=None,
                 Database: DataIntegrationConnectionDatabaseBase = None,
                 BigData: DataIntegrationConnectionBigDataBase = None,
                 File: DataIntegrationConnectionFileBase = None,
                 Queue: DataIntegrationConnectionQueueBase = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SourceOrTarget: int = SourceOrTarget
        self.DataIntegrationId: str = DataIntegrationId
        self.ConnectionId: str = ConnectionId
        self.DataIntegration = DataIntegration
        self.Connection = Connection
        self.Database = Database
        self.BigData = BigData
        self.File = File
        self.Queue = Queue
