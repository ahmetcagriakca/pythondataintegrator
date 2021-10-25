from typing import List
from pdip.cqrs.decorators import responseclass
from domain.connection.LookupConnectorType.LookupConnectorTypeDto import LookupConnectorTypeDto


@responseclass
class LookupConnectorTypeResponse:
	Data: List[LookupConnectorTypeDto] = None
