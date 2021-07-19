from dataclasses import dataclass
from typing import List

from domain.common.decorators.responseclass import responseclass
from domain.operation.GetDataOperationJobList.GetDataOperationJobListDto import GetDataOperationJobListDto


@responseclass
class GetDataOperationJobListResponse:
    Data: List[GetDataOperationJobListDto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None
