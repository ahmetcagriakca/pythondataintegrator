from dataclasses import dataclass

from domain.operation.GetDataOperationJobList.GetDataOperationJobListRequest import GetDataOperationJobListRequest


@dataclass
class GetDataOperationJobListQuery:
    request: GetDataOperationJobListRequest= None
