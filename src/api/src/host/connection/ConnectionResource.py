from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from src.application.connection.DeleteConnection.DeleteConnectionCommand import DeleteConnectionCommand
from src.application.connection.DeleteConnection.DeleteConnectionRequest import DeleteConnectionRequest
from src.application.connection.GetConnectionList.GetConnectionListQuery import GetConnectionListQuery
from src.application.connection.GetConnectionList.GetConnectionListRequest import GetConnectionListRequest
from src.application.connection.GetConnectionList.GetConnectionListResponse import GetConnectionListResponse


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
