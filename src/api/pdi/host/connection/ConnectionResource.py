from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from pdi.application.connection.DeleteConnection.DeleteConnectionCommand import DeleteConnectionCommand
from pdi.application.connection.DeleteConnection.DeleteConnectionRequest import DeleteConnectionRequest
from pdi.application.connection.GetConnection.GetConnectionQuery import GetConnectionQuery
from pdi.application.connection.GetConnection.GetConnectionRequest import GetConnectionRequest
from pdi.application.connection.GetConnection.GetConnectionResponse import GetConnectionResponse
from pdi.application.connection.GetConnectionList.GetConnectionListQuery import GetConnectionListQuery
from pdi.application.connection.GetConnectionList.GetConnectionListRequest import GetConnectionListRequest
from pdi.application.connection.GetConnectionList.GetConnectionListResponse import GetConnectionListResponse


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
