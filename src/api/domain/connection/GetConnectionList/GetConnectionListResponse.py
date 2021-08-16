from typing import List

from infrastructure.cqrs.decorators.responseclass import responseclass
from domain.connection.GetConnectionList.GetConnectionListDto import GetConnectionListDto


@responseclass
class GetConnectionListResponse:
    Data: List[GetConnectionListDto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None