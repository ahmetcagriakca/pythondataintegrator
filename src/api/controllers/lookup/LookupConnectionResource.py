from injector import inject
from domain.connection.LookupConnection.LookupConnectionQuery import LookupConnectionQuery
from domain.connection.LookupConnection.LookupConnectionRequest import LookupConnectionRequest
from domain.connection.LookupConnection.LookupConnectionResponse import LookupConnectionResponse
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher


@controller()
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
