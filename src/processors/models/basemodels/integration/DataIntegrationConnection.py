from models.basemodels.integration.DataIntegrationConnectionDatabase import \
    DataIntegrationConnectionDatabase
from models.basemodels.integration.DataIntegrationConnectionFile import \
    DataIntegrationConnectionFile

from infrastructor.json.JsonConvert import JsonConvert
from models.basemodels.integration.DataIntegrationConnectionQueue import \
    DataIntegrationConnectionQueue


@JsonConvert.register
class DataIntegrationConnection:
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
