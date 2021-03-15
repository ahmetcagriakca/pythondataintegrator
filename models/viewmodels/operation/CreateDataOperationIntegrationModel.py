from infrastructor.json.JsonConvert import JsonConvert
from models.viewmodels.integration.CreateDataIntegrationModel import CreateDataIntegrationModel


@JsonConvert.register
class CreateDataOperationIntegrationModel:
    def __init__(self,
                 Limit: int = None,
                 ProcessCount: int = None,
                 Integration: CreateDataIntegrationModel = None,
                 *args, **kwargs):
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount
        self.Integration: CreateDataIntegrationModel = Integration
