from typing import List
from domain.common.decorators.responseclass import responseclass
from domain.connection.LookupConnection.LookupConnectionDto import LookupConnectionDto


@responseclass
class LookupConnectionResponse:
    Data: List[LookupConnectionDto] = None
