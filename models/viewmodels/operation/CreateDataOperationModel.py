from models.viewmodels.operation.CreateDataOperationContactModel import CreateDataOperationContactModel
from models.viewmodels.operation.CreateDataOperationIntegrationModel import CreateDataOperationIntegrationModel


class CreateDataOperationModel:
    def __init__(self,
                 Name: str = None,
                 Contacts:[CreateDataOperationContactModel]=None,
                 Integrations:[CreateDataOperationIntegrationModel]=None,
                 *args, **kwargs):
        self.Name: str = Name
        self.Contacts: [CreateDataOperationContactModel] = Contacts
        self.Integrations: [CreateDataOperationIntegrationModel] = Integrations