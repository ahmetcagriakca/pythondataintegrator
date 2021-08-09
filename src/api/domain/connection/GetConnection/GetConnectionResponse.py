from infrastructure.cqrs.decorators.responseclass import responseclass
from domain.connection.GetConnection.GetConnectionDto import GetConnectionDto


@responseclass
class GetConnectionResponse:
	Data: GetConnectionDto = None
