from pdip.cqrs.decorators import responseclass

from src.application.connection.GetConnection.GetConnectionDto import GetConnectionDto


@responseclass
class GetConnectionResponse:
    Data: GetConnectionDto = None
