from datetime import datetime

from pdip.cqrs.decorators import dtoclass

@dtoclass
class GetDataOperationScheduleInfoDto:
    Cron: str = None
    StartDate: datetime = None
    EndDate: datetime = None

@dtoclass
class GetDataOperationJobExecutionDto:
    Id: int = None
    JobId: int = None
    DataOperationId: str = None
    DataOperationName: str = None
    ScheduleInfo: GetDataOperationScheduleInfoDto = None
    StatusId: int = None
    StatusDescription: str = None
    Log: str = None
    SourceDataCount: int = None
    AffectedRowCount: int = None
    StartDate: datetime = None
    EndDate: datetime = None
    CreationDate: datetime = None
    LastUpdatedDate: datetime = None
