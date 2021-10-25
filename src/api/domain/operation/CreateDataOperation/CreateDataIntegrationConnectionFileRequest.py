from pdip.cqrs.decorators import requestclass
from domain.operation.CreateDataOperation.CreateDataIntegrationConnectionFileCsvRequest import \
    CreateDataIntegrationConnectionFileCsvRequest


@requestclass
class CreateDataIntegrationConnectionFileRequest:
    Folder: str = None
    FileName: str = None
    Csv: CreateDataIntegrationConnectionFileCsvRequest = None
