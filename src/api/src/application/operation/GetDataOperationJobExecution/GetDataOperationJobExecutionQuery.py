from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionRequest import \
    GetDataOperationJobExecutionRequest
from src.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionResponse import \
    GetDataOperationJobExecutionResponse


@dataclass
class GetDataOperationJobExecutionQuery(IQuery[GetDataOperationJobExecutionResponse]):
    request: GetDataOperationJobExecutionRequest = None
