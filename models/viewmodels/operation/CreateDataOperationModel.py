from models.viewmodels.operation.CreateDataOperationIntegrationModel import CreateDataOperationIntegrationModel


class CreateDataOperationModel:
    def __init__(self,
                 Name: str = None,
                 Integrations:[CreateDataOperationIntegrationModel]=None,
                 Limit: int = None,
                 ProcessCount: int = None,
                 *args, **kwargs):
        self.Name: str = Name
        self.Integrations: [CreateDataOperationIntegrationModel] = Integrations
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount