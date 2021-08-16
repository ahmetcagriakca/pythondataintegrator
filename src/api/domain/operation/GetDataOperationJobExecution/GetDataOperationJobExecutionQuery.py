from dataclasses import dataclass
from infrastructure.cqrs.IQuery import IQuery
from domain.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionRequest import GetDataOperationJobExecutionRequest
from domain.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionResponse import GetDataOperationJobExecutionResponse


@dataclass
class GetDataOperationJobExecutionQuery(IQuery[GetDataOperationJobExecutionResponse]):
    request: GetDataOperationJobExecutionRequest = None