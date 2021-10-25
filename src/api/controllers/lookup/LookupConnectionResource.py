from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from domain.connection.LookupConnection.LookupConnectionQuery import LookupConnectionQuery
from domain.connection.LookupConnection.LookupConnectionRequest import LookupConnectionRequest
from domain.connection.LookupConnection.LookupConnectionResponse import LookupConnectionResponse


class LookupConnectionResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: LookupConnectionRequest) -> LookupConnectionResponse:
        """
        Get All Connections
        """
        query = LookupConnectionQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result
