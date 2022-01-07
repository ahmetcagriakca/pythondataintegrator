from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.connection.LookupAuthenticationType.LookupAuthenticationTypeRequest import \
    LookupAuthenticationTypeRequest
from pdi.application.connection.LookupAuthenticationType.LookupAuthenticationTypeResponse import \
    LookupAuthenticationTypeResponse


@dataclass
class LookupAuthenticationTypeQuery(IQuery[LookupAuthenticationTypeResponse]):
    request: LookupAuthenticationTypeRequest = None
