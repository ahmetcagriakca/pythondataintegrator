from typing import Optional

from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.operation.GetDataOperationJobList.GetDataOperationJobListRequest import \
    GetDataOperationJobListRequest
from src.application.operation.GetDataOperationJobList.GetDataOperationJobListResponse import \
    GetDataOperationJobListResponse


@dataclass
class GetDataOperationJobListQuery(IQuery[GetDataOperationJobListResponse]):
    request: GetDataOperationJobListRequest = None
    OnlyCron: Optional[bool] = None
