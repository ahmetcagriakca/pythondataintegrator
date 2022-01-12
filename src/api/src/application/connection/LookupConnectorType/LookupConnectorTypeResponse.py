from typing import List

from pdip.cqrs.decorators import responseclass

from src.application.connection.LookupConnectorType.LookupConnectorTypeDto import LookupConnectorTypeDto


@responseclass
class LookupConnectorTypeResponse:
    Data: List[LookupConnectorTypeDto] = None
