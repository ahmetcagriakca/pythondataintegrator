from typing import List
from infrastructure.cqrs.decorators.responseclass import responseclass
from domain.connection.LookupConnectionType.LookupConnectionTypeDto import LookupConnectionTypeDto


@responseclass
class LookupConnectionTypeResponse:
	Data: List[LookupConnectionTypeDto] = None
