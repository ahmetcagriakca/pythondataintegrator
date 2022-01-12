from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.connection.LookupConnectionType.LookupConnectionTypeRequest import LookupConnectionTypeRequest
from src.application.connection.LookupConnectionType.LookupConnectionTypeResponse import LookupConnectionTypeResponse


@dataclass
class LookupConnectionTypeQuery(IQuery[LookupConnectionTypeResponse]):
    request: LookupConnectionTypeRequest = None
