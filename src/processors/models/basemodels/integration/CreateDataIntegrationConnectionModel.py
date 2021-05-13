from models.viewmodels.integration.DataIntegrationConnectionDatabase import \
    DataIntegrationConnectionDatabase
from models.viewmodels.integration.DataIntegrationConnectionFile import \
    DataIntegrationConnectionFile

from infrastructor.json.JsonConvert import JsonConvert
from models.viewmodels.integration.DataIntegrationConnectionQueue import \
    DataIntegrationConnectionQueue


@JsonConvert.register
class CreateDataIntegrationConnectionModel:
    def __init__(self,
                 ConnectionName: str = None,
                 Database: DataIntegrationConnectionDatabase = None,
                 File: DataIntegrationConnectionFile = None,
                 Queue: DataIntegrationConnectionQueue=None,
                 Columns: str = None,
                 ):
        self.Queue = Queue
        self.ConnectionName: str = ConnectionName
        self.File = File
        self.Database = Database
        self.Columns: str = Columns
