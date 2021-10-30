from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionRequest import \
    GetDataOperationJobExecutionRequest
from pdi.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionResponse import \
    GetDataOperationJobExecutionResponse


@dataclass
class GetDataOperationJobExecutionQuery(IQuery[GetDataOperationJobExecutionResponse]):
    request: GetDataOperationJobExecutionRequest = None
