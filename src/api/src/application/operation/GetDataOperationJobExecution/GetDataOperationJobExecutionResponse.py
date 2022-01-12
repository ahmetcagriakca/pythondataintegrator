from pdip.cqrs.decorators import responseclass

from src.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionDto import \
    GetDataOperationJobExecutionDto


@responseclass
class GetDataOperationJobExecutionResponse:
    Data: GetDataOperationJobExecutionDto = None
