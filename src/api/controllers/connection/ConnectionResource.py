from domain.connection.DeleteConnection.DeleteConnectionCommand import DeleteConnectionCommand
from domain.connection.GetConnectionList.GetConnectionListQuery import GetConnectionListQuery
from domain.connection.GetConnectionList.GetConnectionListRequest import GetConnectionListRequest
from domain.connection.GetConnectionList.GetConnectionListResponse import GetConnectionListResponse
from infrastructure.cqrs.Dispatcher import Dispatcher
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.api.decorators.Controller import controller
from injector import inject

@controller()
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

    def delete(self, Id: int):
        """
        Delete Existing Connection
        """
        command = DeleteConnectionCommand(Id=Id)
        self.dispatcher.dispatch(command)
        return "Connection deleted"
