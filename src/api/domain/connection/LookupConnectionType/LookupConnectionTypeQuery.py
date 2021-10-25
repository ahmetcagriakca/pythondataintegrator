from dataclasses import dataclass
from pdip.cqrs import IQuery
from domain.connection.LookupConnectionType.LookupConnectionTypeRequest import LookupConnectionTypeRequest
from domain.connection.LookupConnectionType.LookupConnectionTypeResponse import LookupConnectionTypeResponse


@dataclass
class LookupConnectionTypeQuery(IQuery[LookupConnectionTypeResponse]):
    request: LookupConnectionTypeRequest = None
