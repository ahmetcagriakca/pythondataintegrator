from typing import List
from infrastructure.cqrs.decorators.responseclass import responseclass
from domain.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListDto import GetDataOperationJobExecutionListDto


@responseclass
class GetDataOperationJobExecutionListResponse:
    Data: List[GetDataOperationJobExecutionListDto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None