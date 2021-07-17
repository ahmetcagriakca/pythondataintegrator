from typing import List

from domain.common.decorators.requestclass import requestclass
from domain.operation.CreateDataOperation.CreateDataOperationContactRequest import CreateDataOperationContactRequest
from domain.operation.CreateDataOperation.CreateDataOperationIntegrationRequest import CreateDataOperationIntegrationRequest


@requestclass
class CreateDataOperationRequest:
    Name: str = None
    Contacts: List[CreateDataOperationContactRequest] = None
    Integrations: List[CreateDataOperationIntegrationRequest] = None
