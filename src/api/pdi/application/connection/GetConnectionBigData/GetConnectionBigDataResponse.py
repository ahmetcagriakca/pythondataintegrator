from pdip.cqrs.decorators import responseclass

from pdi.application.connection.GetConnectionBigData.GetConnectionBigDataDto import GetConnectionBigDataDto


@responseclass
class GetConnectionBigDataResponse:
    Data: GetConnectionBigDataDto = None
