from injector import inject
from domain.connection.GetConnectionList.GetConnectionListQuery import GetConnectionListQuery
from domain.connection.GetConnectionList.GetConnectionListQueryHandler import GetConnectionListQueryHandler
from domain.connection.GetConnectionList.GetConnectionListRequest import GetConnectionListRequest
from domain.connection.GetConnectionList.GetConnectionListResponse import GetConnectionListResponse
from domain.connection.services.ConnectionService import ConnectionService
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.api.decorators.Controller import controller


@controller()
class ConnectionResource(ResourceBase):
    @inject
    def __init__(self,
                 connection_service: ConnectionService,
                 connection_list_query_handler: GetConnectionListQueryHandler,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_list_query_handler = connection_list_query_handler
        self.connection_service = connection_service

    def get(self, req: GetConnectionListRequest) -> GetConnectionListResponse:
        """
        Get All Connections
        """
        query = GetConnectionListQuery(request=req)
        res = self.connection_list_query_handler.handle(query=query)
        return res

    def delete(self, Id:int):
        """
        Delete Existing Database Connection
        """
        # data = IocManager.api.payload
        # id = data.get('Id')  #
        deletion_result = self.connection_service.delete_connection(Id)
        return deletion_result
