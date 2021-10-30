from pdip.cqrs.decorators import responseclass

from pdi.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionDto import \
    GetDataOperationJobExecutionDto


@responseclass
class GetDataOperationJobExecutionResponse:
    Data: GetDataOperationJobExecutionDto = None
