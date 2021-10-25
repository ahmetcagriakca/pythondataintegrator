from dataclasses import dataclass

from domain.operation.GetDataOperationList.GetDataOperationListRequest import GetDataOperationListRequest
from domain.operation.GetDataOperationList.GetDataOperationListResponse import GetDataOperationListResponse
from pdip.cqrs import IQuery


@dataclass
class GetDataOperationListQuery(IQuery[GetDataOperationListResponse]):
    request: GetDataOperationListRequest = None
