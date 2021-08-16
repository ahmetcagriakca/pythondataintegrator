from infrastructure.cqrs.decorators.requestclass import requestclass
from domain.operation.CreateDataOperation.CreateDataIntegrationConnectionRequest import \
    CreateDataIntegrationConnectionRequest


@requestclass
class CreateDataIntegrationRequest:
    Code: str = None
    SourceConnections: CreateDataIntegrationConnectionRequest = None
    TargetConnections: CreateDataIntegrationConnectionRequest = None
    IsTargetTruncate: bool = None
    IsDelta: bool = None
    Comments: str = None
