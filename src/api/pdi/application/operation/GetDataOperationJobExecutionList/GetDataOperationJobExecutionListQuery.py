from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListRequest import \
    GetDataOperationJobExecutionListRequest
from pdi.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListResponse import \
    GetDataOperationJobExecutionListResponse


@dataclass
class GetDataOperationJobExecutionListQuery(IQuery[GetDataOperationJobExecutionListResponse]):
    request: GetDataOperationJobExecutionListRequest = None
