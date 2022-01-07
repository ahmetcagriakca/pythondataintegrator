from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from pdi.application.connection.LookupAuthenticationType.LookupAuthenticationTypeQuery import \
    LookupAuthenticationTypeQuery
from pdi.application.connection.LookupAuthenticationType.LookupAuthenticationTypeRequest import \
    LookupAuthenticationTypeRequest
from pdi.application.connection.LookupAuthenticationType.LookupAuthenticationTypeResponse import \
    LookupAuthenticationTypeResponse


class LookupAuthenticationTypeResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: LookupAuthenticationTypeRequest) -> LookupAuthenticationTypeResponse:
        """
        Get All Connection Types
        """
        query = LookupAuthenticationTypeQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result
