from models.viewmodels.integration.CreateDataIntegrationConnectionDatabaseModel import \
    CreateDataIntegrationConnectionDatabaseModel
from models.viewmodels.integration.CreateDataIntegrationConnectionFileModel import \
    CreateDataIntegrationConnectionFileModel

from infrastructor.json.JsonConvert import JsonConvert
from models.viewmodels.integration.CreateDataIntegrationConnectionQueueModel import \
    CreateDataIntegrationConnectionQueueModel


@JsonConvert.register
class CreateDataIntegrationConnectionModel:
    def __init__(self,
                 ConnectionName: str = None,
                 Database: CreateDataIntegrationConnectionDatabaseModel = None,
                 File: CreateDataIntegrationConnectionFileModel = None,
                 Queue: CreateDataIntegrationConnectionQueueModel=None,
                 Columns: str = None,
                 ):
        self.Queue = Queue
        self.ConnectionName: str = ConnectionName
        self.File = File
        self.Database = Database
        self.Columns: str = Columns
