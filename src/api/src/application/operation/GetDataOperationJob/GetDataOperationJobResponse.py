from pdip.cqrs.decorators import responseclass

from src.application.operation.GetDataOperationJob.GetDataOperationJobDto import GetDataOperationJobDto


@responseclass
class GetDataOperationJobResponse:
    Data: GetDataOperationJobDto = None
