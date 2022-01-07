from typing import List

from pdip.cqrs.decorators import responseclass

from pdi.application.connection.LookupAuthenticationType.LookupAuthenticationTypeDto import LookupAuthenticationTypeDto


@responseclass
class LookupAuthenticationTypeResponse:
    Data: List[LookupAuthenticationTypeDto] = None
