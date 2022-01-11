from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from src.application.connection.GetConnection.GetConnectionQuery import GetConnectionQuery
from src.application.connection.GetConnection.GetConnectionRequest import GetConnectionRequest
from src.application.connection.GetConnection.GetConnectionResponse import GetConnectionResponse


class ConnectionByIdResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: GetConnectionRequest) -> GetConnectionResponse:
        """
        Get Data Operation Job By Id
        """
        query = GetConnectionQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result
