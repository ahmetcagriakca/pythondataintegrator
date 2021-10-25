from datetime import datetime

from pdip.cqrs.decorators import dtoclass


@dtoclass
class GetDataOperationJobExecutionLogListDto:
    Id: int = None
    CreationDate: datetime = None
    Comments: str = None
    Content: str = None
