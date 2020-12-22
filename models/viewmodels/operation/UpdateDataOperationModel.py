from models.viewmodels.operation.UpdateDataOperationIntegrationModel import UpdateDataOperationIntegrationModel


class UpdateDataOperationModel:
    def __init__(self,
                 Id: int = None,
                 Name: str = None,
                 Integrations:[UpdateDataOperationIntegrationModel]=None,
                 *args, **kwargs):
        self.Id: int = Id
        self.Name: str = Name
        self.Integrations: [UpdateDataOperationIntegrationModel] = Integrations