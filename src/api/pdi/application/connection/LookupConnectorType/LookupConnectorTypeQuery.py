from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.connection.LookupConnectorType.LookupConnectorTypeRequest import LookupConnectorTypeRequest
from pdi.application.connection.LookupConnectorType.LookupConnectorTypeResponse import LookupConnectorTypeResponse


@dataclass
class LookupConnectorTypeQuery(IQuery[LookupConnectorTypeResponse]):
    request: LookupConnectorTypeRequest = None
