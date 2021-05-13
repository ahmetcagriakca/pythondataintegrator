from infrastructor.json.JsonConvert import JsonConvert
from models.basemodels.integration import DataIntegrationConnectionFileCsv


@JsonConvert.register
class DataIntegrationConnectionFile:
    def __init__(self,
                 Folder: str = None,
                 FileName: str = None,
                 Csv: DataIntegrationConnectionFileCsv = None
                 ):
        self.Folder: str = Folder
        self.FileName: str = FileName
        self.Csv: DataIntegrationConnectionFileCsv = Csv
