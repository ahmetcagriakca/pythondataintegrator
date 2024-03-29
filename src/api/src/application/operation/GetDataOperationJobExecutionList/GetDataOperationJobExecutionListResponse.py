from typing import List

from pdip.cqrs.decorators import responseclass

from src.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListDto import \
    GetDataOperationJobExecutionListDto


@responseclass
class GetDataOperationJobExecutionListResponse:
    Data: List[GetDataOperationJobExecutionListDto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None
