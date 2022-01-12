from typing import List

from pdip.cqrs.decorators import responseclass

from src.application.operation.GetDataOperationJobList.GetDataOperationJobListDto import GetDataOperationJobListDto


@responseclass
class GetDataOperationJobListResponse:
    Data: List[GetDataOperationJobListDto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None
