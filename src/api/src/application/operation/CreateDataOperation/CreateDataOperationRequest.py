from typing import List

from pdip.cqrs.decorators import requestclass

from src.application.operation.CreateDataOperation.CreateDataOperationContactRequest import \
    CreateDataOperationContactRequest
from src.application.operation.CreateDataOperation.CreateDataOperationIntegrationRequest import \
    CreateDataOperationIntegrationRequest


@requestclass
class CreateDataOperationRequest:
    Name: str = None
    Contacts: List[CreateDataOperationContactRequest] = None
    Integrations: List[CreateDataOperationIntegrationRequest] = None
