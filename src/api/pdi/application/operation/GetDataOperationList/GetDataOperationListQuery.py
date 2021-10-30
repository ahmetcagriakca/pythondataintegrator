from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.operation.GetDataOperationList.GetDataOperationListRequest import GetDataOperationListRequest
from pdi.application.operation.GetDataOperationList.GetDataOperationListResponse import GetDataOperationListResponse


@dataclass
class GetDataOperationListQuery(IQuery[GetDataOperationListResponse]):
    request: GetDataOperationListRequest = None
