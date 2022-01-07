from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.operation.GetDataOperationList.GetDataOperationListRequest import GetDataOperationListRequest
from src.application.operation.GetDataOperationList.GetDataOperationListResponse import GetDataOperationListResponse


@dataclass
class GetDataOperationListQuery(IQuery[GetDataOperationListResponse]):
    request: GetDataOperationListRequest = None
