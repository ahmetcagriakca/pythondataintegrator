from dataclasses import dataclass

from domain.operation.GetDataOperationList.GetDataOperationListRequest import GetDataOperationListRequest


@dataclass
class GetDataOperationListQuery:
    request: GetDataOperationListRequest = None
