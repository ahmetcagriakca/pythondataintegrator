from typing import List
from infrastructure.cqrs.decorators.responseclass import responseclass
from domain.operation.GetDataOperationList.GetDataOperationListDto import GetDataOperationListDto


@responseclass
class GetDataOperationListResponse:
    Data: List[GetDataOperationListDto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None
