from pdip.cqrs.decorators import requestclass

from src.application.operation.CreateDataOperation.CreateDataIntegrationConnectionBigDataRequest import \
    CreateDataIntegrationConnectionBigDataRequest
from src.application.operation.CreateDataOperation.CreateDataIntegrationConnectionDatabaseRequest import \
    CreateDataIntegrationConnectionDatabaseRequest
from src.application.operation.CreateDataOperation.CreateDataIntegrationConnectionFileRequest import \
    CreateDataIntegrationConnectionFileRequest
from src.application.operation.CreateDataOperation.CreateDataIntegrationConnectionQueueRequest import \
    CreateDataIntegrationConnectionQueueRequest


@requestclass
class CreateDataIntegrationConnectionRequest:
    ConnectionName: str = None
    Database: CreateDataIntegrationConnectionDatabaseRequest = None
    BigData: CreateDataIntegrationConnectionBigDataRequest = None
    File: CreateDataIntegrationConnectionFileRequest = None
    Queue: CreateDataIntegrationConnectionQueueRequest = None
    Columns: str = None
