from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from domain.connection.LookupConnectionType.LookupConnectionTypeQuery import LookupConnectionTypeQuery
from domain.connection.LookupConnectionType.LookupConnectionTypeRequest import LookupConnectionTypeRequest
from domain.connection.LookupConnectionType.LookupConnectionTypeResponse import LookupConnectionTypeResponse


class LookupConnectionTypeResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: LookupConnectionTypeRequest) -> LookupConnectionTypeResponse:
        """
        Get All Connection Types
        """
        query = LookupConnectionTypeQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result
