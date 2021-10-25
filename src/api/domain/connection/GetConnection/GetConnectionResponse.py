from pdip.cqrs.decorators import responseclass
from domain.connection.GetConnection.GetConnectionDto import GetConnectionDto


@responseclass
class GetConnectionResponse:
	Data: GetConnectionDto = None
