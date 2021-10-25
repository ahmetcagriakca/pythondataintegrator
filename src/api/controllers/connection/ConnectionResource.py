from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from domain.connection.DeleteConnection.DeleteConnectionCommand import DeleteConnectionCommand
from domain.connection.DeleteConnection.DeleteConnectionRequest import DeleteConnectionRequest
from domain.connection.GetConnection.GetConnectionQuery import GetConnectionQuery
from domain.connection.GetConnection.GetConnectionRequest import GetConnectionRequest
from domain.connection.GetConnection.GetConnectionResponse import GetConnectionResponse
from domain.connection.GetConnectionList.GetConnectionListQuery import GetConnectionListQuery
from domain.connection.GetConnectionList.GetConnectionListRequest import GetConnectionListRequest
from domain.connection.GetConnectionList.GetConnectionListResponse import GetConnectionListResponse


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


class ConnectionResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: GetConnectionListRequest) -> GetConnectionListResponse:
        """
        Get All Connections
        """
        query = GetConnectionListQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result

    def delete(self, req: DeleteConnectionRequest):
        """
        Delete Existing Connection
        """
        command = DeleteConnectionCommand(request=req)
        self.dispatcher.dispatch(command)
