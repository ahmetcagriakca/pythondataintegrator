from typing import List

from pdip.cqrs.decorators import responseclass

from pdi.application.connection.LookupConnectorType.LookupConnectorTypeDto import LookupConnectorTypeDto


@responseclass
class LookupConnectorTypeResponse:
    Data: List[LookupConnectorTypeDto] = None
