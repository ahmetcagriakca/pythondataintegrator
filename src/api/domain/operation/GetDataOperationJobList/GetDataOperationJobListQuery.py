from dataclasses import dataclass
from typing import Optional

from domain.operation.GetDataOperationJobList.GetDataOperationJobListRequest import GetDataOperationJobListRequest
from domain.operation.GetDataOperationJobList.GetDataOperationJobListResponse import GetDataOperationJobListResponse
from pdip.cqrs import IQuery


@dataclass
class GetDataOperationJobListQuery(IQuery[GetDataOperationJobListResponse]):
    request: GetDataOperationJobListRequest= None
    OnlyCron: Optional[bool] = None
