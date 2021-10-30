from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListRequest import \
    GetDataOperationJobExecutionLogListRequest
from pdi.application.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListResponse import \
    GetDataOperationJobExecutionLogListResponse


@dataclass
class GetDataOperationJobExecutionLogListQuery(IQuery[GetDataOperationJobExecutionLogListResponse]):
    request: GetDataOperationJobExecutionLogListRequest = None
