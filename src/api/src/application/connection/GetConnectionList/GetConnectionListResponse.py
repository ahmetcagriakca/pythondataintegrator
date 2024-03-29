from typing import List

from pdip.cqrs.decorators import responseclass

from src.application.connection.GetConnectionList.GetConnectionListDto import GetConnectionListDto


@responseclass
class GetConnectionListResponse:
    Data: List[GetConnectionListDto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None
