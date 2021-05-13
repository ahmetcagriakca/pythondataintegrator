from typing import List

from infrastructor.json.JsonConvert import JsonConvert
from models.viewmodels.operation.DataOperationContact import DataOperationContact
from models.viewmodels.operation.DataOperationIntegration import DataOperationIntegration


@JsonConvert.register
class DataOperation:
    def __init__(self,
                 Name: str = None,
                 Contacts: List[DataOperationContact] = None,
                 Integrations: List[DataOperationIntegration] = None,
                 *args, **kwargs):
        self.Name: str = Name
        self.Contacts: List[DataOperationContact] = Contacts
        self.Integrations: List[DataOperationIntegration] = Integrations
