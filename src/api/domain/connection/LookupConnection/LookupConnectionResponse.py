from typing import List
from infrastructure.cqrs.decorators.responseclass import responseclass
from domain.connection.LookupConnection.LookupConnectionDto import LookupConnectionDto


@responseclass
class LookupConnectionResponse:
    Data: List[LookupConnectionDto] = None
