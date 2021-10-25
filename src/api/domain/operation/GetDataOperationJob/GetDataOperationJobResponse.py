from pdip.cqrs.decorators import responseclass
from domain.operation.GetDataOperationJob.GetDataOperationJobDto import GetDataOperationJobDto


@responseclass
class GetDataOperationJobResponse:
	Data: GetDataOperationJobDto = None
