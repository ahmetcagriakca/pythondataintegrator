from pdip.cqrs.decorators import responseclass

from src.application.operation.GetDataOperation.GetDataOperationDto import GetDataOperationDto


@responseclass
class GetDataOperationResponse:
    Data: GetDataOperationDto = None
