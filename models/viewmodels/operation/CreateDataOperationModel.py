from models.viewmodels.operation.CreateDataOperationIntegrationModel import CreateDataOperationIntegrationModel


class CreateDataOperationModel:
    def __init__(self,
                 Name: str = None,
                 Integrations:[CreateDataOperationIntegrationModel]=None,
                 *args, **kwargs):
        self.Name: str = Name
        self.Integrations: [CreateDataOperationIntegrationModel] = Integrations