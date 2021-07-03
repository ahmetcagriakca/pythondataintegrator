from infrastructor.json.JsonConvert import JsonConvert
from models.viewmodels.integration import CreateDataIntegrationConnectionFileCsvModel


@JsonConvert.register
class CreateDataIntegrationConnectionFileModel:
    def __init__(self,
                 Folder: str = None,
                 FileName: str = None,
                 Csv: CreateDataIntegrationConnectionFileCsvModel = None
                 ):
        self.Folder: str = Folder
        self.FileName: str = FileName
        self.Csv: CreateDataIntegrationConnectionFileCsvModel = Csv
