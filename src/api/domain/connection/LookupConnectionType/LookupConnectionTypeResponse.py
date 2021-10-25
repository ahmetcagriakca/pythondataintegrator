from typing import List
from pdip.cqrs.decorators import responseclass
from domain.connection.LookupConnectionType.LookupConnectionTypeDto import LookupConnectionTypeDto


@responseclass
class LookupConnectionTypeResponse:
	Data: List[LookupConnectionTypeDto] = None
