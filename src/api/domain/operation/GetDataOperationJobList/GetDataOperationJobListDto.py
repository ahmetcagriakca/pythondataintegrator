import datetime
from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class GetDataOperationJobListDto:
    Id: int = None
    JobId: int = None
    DataOperationId: str = None
    DataOperationName: str = None
    Cron: str = None
    StartDate: datetime.datetime = None
    EndDate: datetime.datetime = None
    NextRunTime: datetime.datetime = None
    CreationDate: datetime.datetime = None
    LastUpdatedDate: datetime.datetime = None
    IsDeleted: int = None
