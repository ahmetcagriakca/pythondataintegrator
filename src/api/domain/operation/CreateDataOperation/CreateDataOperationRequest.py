from typing import List

from pdip.cqrs.decorators import requestclass
from domain.operation.CreateDataOperation.CreateDataOperationContactRequest import CreateDataOperationContactRequest
from domain.operation.CreateDataOperation.CreateDataOperationIntegrationRequest import CreateDataOperationIntegrationRequest


@requestclass
class CreateDataOperationRequest:
    Name: str = None
    Contacts: List[CreateDataOperationContactRequest] = None
    Integrations: List[CreateDataOperationIntegrationRequest] = None
