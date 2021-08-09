from infrastructure.cqrs.decorators.responseclass import responseclass
from domain.operation.GetDataOperationJob.GetDataOperationJobDto import GetDataOperationJobDto


@responseclass
class GetDataOperationJobResponse:
	Data: GetDataOperationJobDto = None
