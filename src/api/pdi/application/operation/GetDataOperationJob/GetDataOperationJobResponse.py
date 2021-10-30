from pdip.cqrs.decorators import responseclass

from pdi.application.operation.GetDataOperationJob.GetDataOperationJobDto import GetDataOperationJobDto


@responseclass
class GetDataOperationJobResponse:
    Data: GetDataOperationJobDto = None
