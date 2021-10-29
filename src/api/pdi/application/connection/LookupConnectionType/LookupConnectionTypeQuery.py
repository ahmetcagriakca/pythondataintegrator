from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.connection.LookupConnectionType.LookupConnectionTypeRequest import LookupConnectionTypeRequest
from pdi.application.connection.LookupConnectionType.LookupConnectionTypeResponse import LookupConnectionTypeResponse


@dataclass
class LookupConnectionTypeQuery(IQuery[LookupConnectionTypeResponse]):
    request: LookupConnectionTypeRequest = None
