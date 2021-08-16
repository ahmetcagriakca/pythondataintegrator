from datetime import datetime

from infrastructure.cqrs.decorators.dtoclass import dtoclass


@dtoclass
class GetDataOperationJobExecutionLogListDto:
    Id: int = None
    CreationDate: datetime = None
    Comments: str = None
    Content: str = None
