from pdip.cqrs.decorators import responseclass
from domain.operation.GetDataOperation.GetDataOperationDto import GetDataOperationDto


@responseclass
class GetDataOperationResponse:
	Data: GetDataOperationDto = None
