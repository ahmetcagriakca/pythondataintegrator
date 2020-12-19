from models.viewmodels.operation.UpdateDataOperationIntegrationModel import UpdateDataOperationIntegrationModel


class UpdateDataOperationModel:
    def __init__(self,
                 Id: int = None,
                 Name: str = None,
                 Integrations:[UpdateDataOperationIntegrationModel]=None,
                 Limit: int = None,
                 ProcessCount: int = None,
                 *args, **kwargs):
        self.Id: int = Id
        self.Name: str = Name
        self.Integrations: [UpdateDataOperationIntegrationModel] = Integrations
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount