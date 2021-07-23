from typing import List
from domain.common.decorators.responseclass import responseclass
from domain.connection.GetConnection.GetConnectionDto import GetConnectionDto


@responseclass
class GetConnectionResponse:
	Data: GetConnectionDto = None
