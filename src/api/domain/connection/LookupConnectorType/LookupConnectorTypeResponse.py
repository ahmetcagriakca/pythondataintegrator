from typing import List
from domain.common.decorators.responseclass import responseclass
from domain.connection.LookupConnectorType.LookupConnectorTypeDto import LookupConnectorTypeDto


@responseclass
class LookupConnectorTypeResponse:
	Data: List[LookupConnectorTypeDto] = None
