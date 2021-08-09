from infrastructure.cqrs.decorators.requestclass import requestclass
from domain.operation.CreateDataOperation.CreateDataIntegrationRequest import CreateDataIntegrationRequest


@requestclass
class CreateDataOperationIntegrationRequest:
    Limit: int = None
    ProcessCount: int = None
    Integration: CreateDataIntegrationRequest = None