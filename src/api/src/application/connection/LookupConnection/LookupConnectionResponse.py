from typing import List

from pdip.cqrs.decorators import responseclass

from src.application.connection.LookupConnection.LookupConnectionDto import LookupConnectionDto


@responseclass
class LookupConnectionResponse:
    Data: List[LookupConnectionDto] = None
