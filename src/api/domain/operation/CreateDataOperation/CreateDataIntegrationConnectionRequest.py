from infrastructure.cqrs.decorators.requestclass import requestclass
from domain.operation.CreateDataOperation.CreateDataIntegrationConnectionDatabaseRequest import \
    CreateDataIntegrationConnectionDatabaseRequest
from domain.operation.CreateDataOperation.CreateDataIntegrationConnectionFileRequest import \
    CreateDataIntegrationConnectionFileRequest
from domain.operation.CreateDataOperation.CreateDataIntegrationConnectionQueueRequest import \
    CreateDataIntegrationConnectionQueueRequest


@requestclass
class CreateDataIntegrationConnectionRequest:
    ConnectionName: str = None
    Database: CreateDataIntegrationConnectionDatabaseRequest = None
    File: CreateDataIntegrationConnectionFileRequest = None
    Queue: CreateDataIntegrationConnectionQueueRequest = None
    Columns: str = None
