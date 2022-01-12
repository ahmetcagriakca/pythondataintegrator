from typing import List

from pdip.cqrs.decorators import responseclass

from src.application.operation.GetDataOperationList.GetDataOperationListDto import GetDataOperationListDto


@responseclass
class GetDataOperationListResponse:
    Data: List[GetDataOperationListDto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None
