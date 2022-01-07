from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.connection.LookupAuthenticationType.LookupAuthenticationTypeRequest import \
    LookupAuthenticationTypeRequest
from src.application.connection.LookupAuthenticationType.LookupAuthenticationTypeResponse import \
    LookupAuthenticationTypeResponse


@dataclass
class LookupAuthenticationTypeQuery(IQuery[LookupAuthenticationTypeResponse]):
    request: LookupAuthenticationTypeRequest = None
