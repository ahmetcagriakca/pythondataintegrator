from dataclasses import dataclass
from pdip.cqrs import IQuery
from domain.connection.LookupConnectorType.LookupConnectorTypeRequest import LookupConnectorTypeRequest
from domain.connection.LookupConnectorType.LookupConnectorTypeResponse import LookupConnectorTypeResponse


@dataclass
class LookupConnectorTypeQuery(IQuery[LookupConnectorTypeResponse]):
    request: LookupConnectorTypeRequest = None
