from pdip.cqrs.decorators import responseclass

from src.application.connection.GetConnectionBigData.GetConnectionBigDataDto import GetConnectionBigDataDto


@responseclass
class GetConnectionBigDataResponse:
    Data: GetConnectionBigDataDto = None
