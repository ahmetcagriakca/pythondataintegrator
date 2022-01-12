from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.connection.LookupConnectorType.LookupConnectorTypeRequest import LookupConnectorTypeRequest
from src.application.connection.LookupConnectorType.LookupConnectorTypeResponse import LookupConnectorTypeResponse


@dataclass
class LookupConnectorTypeQuery(IQuery[LookupConnectorTypeResponse]):
    request: LookupConnectorTypeRequest = None
