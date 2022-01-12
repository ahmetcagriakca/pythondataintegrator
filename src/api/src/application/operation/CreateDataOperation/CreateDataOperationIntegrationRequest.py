from pdip.cqrs.decorators import requestclass

from src.application.operation.CreateDataOperation.CreateDataIntegrationRequest import CreateDataIntegrationRequest


@requestclass
class CreateDataOperationIntegrationRequest:
    Limit: int = None
    ProcessCount: int = None
    Integration: CreateDataIntegrationRequest = None
