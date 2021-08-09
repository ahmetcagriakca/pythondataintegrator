from typing import List
from infrastructure.cqrs.decorators.responseclass import responseclass
from domain.connection.LookupConnectorType.LookupConnectorTypeDto import LookupConnectorTypeDto


@responseclass
class LookupConnectorTypeResponse:
	Data: List[LookupConnectorTypeDto] = None
