from pdip.cqrs.decorators import responseclass

from pdi.application.connection.GetConnection.GetConnectionDto import GetConnectionDto


@responseclass
class GetConnectionResponse:
    Data: GetConnectionDto = None
