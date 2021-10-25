from dataclasses import dataclass
from pdip.cqrs import IQuery
from domain.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListRequest import GetDataOperationJobExecutionLogListRequest
from domain.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListResponse import GetDataOperationJobExecutionLogListResponse


@dataclass
class GetDataOperationJobExecutionLogListQuery(IQuery[GetDataOperationJobExecutionLogListResponse]):
    request: GetDataOperationJobExecutionLogListRequest = None
