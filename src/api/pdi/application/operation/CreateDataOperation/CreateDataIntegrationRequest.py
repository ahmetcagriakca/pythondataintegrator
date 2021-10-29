from pdip.cqrs.decorators import requestclass

from pdi.application.operation.CreateDataOperation.CreateDataIntegrationConnectionRequest import \
    CreateDataIntegrationConnectionRequest


@requestclass
class CreateDataIntegrationRequest:
    Code: str = None
    SourceConnections: CreateDataIntegrationConnectionRequest = None
    TargetConnections: CreateDataIntegrationConnectionRequest = None
    IsTargetTruncate: bool = None
    IsDelta: bool = None
    Comments: str = None
