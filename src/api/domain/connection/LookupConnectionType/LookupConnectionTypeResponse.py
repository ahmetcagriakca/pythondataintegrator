from typing import List
from domain.common.decorators.responseclass import responseclass
from domain.connection.LookupConnectionType.LookupConnectionTypeDto import LookupConnectionTypeDto


@responseclass
class LookupConnectionTypeResponse:
	Data: List[LookupConnectionTypeDto] = None
