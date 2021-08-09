from datetime import datetime

from infrastructure.cqrs.decorators.dtoclass import dtoclass


@dtoclass
class GetDataOperationJobExecutionIntegrationListDto:
    Id: int = None
    DataIntegrationId: int = None
    DataIntegrationCode: str = None
    Order: int = None
    SourceConnectionName: str = None
    TargetConnectionName: str = None
    StatusId: int = None
    StatusDescription: str = None
    Status: str = None
    Limit: int = None
    ProcessCount: int = None
    AffectedRowCount: int = None
    SourceDataCount: int = None
    StartDate: datetime = None
    EndDate: datetime = None
    CreationDate: datetime = None
    Log: str = None
