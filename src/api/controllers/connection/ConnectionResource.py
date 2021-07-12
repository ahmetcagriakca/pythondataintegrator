import json
from flask import request
from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.connection.models.ConnectionModels import ConnectionModels
from domain.connection.GetConnectionList.ConnectionListQuery import ConnectionListQuery
from domain.connection.GetConnectionList.ConnectionListQueryHandler import ConnectionListQueryHandler
from domain.connection.GetConnectionList.ConnectionListRequest import ConnectionListRequest
from domain.connection.services.ConnectionService import ConnectionService
from IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.json.DateTimeEncoder import DateTimeEncoder
from infrastructor.json.JsonConvert import JsonConvert


@ConnectionModels.ns.route("")
class ConnectionResource(ResourceBase):
    @inject
    def __init__(self,
                 connection_service: ConnectionService,
                 connection_list_query_handler: ConnectionListQueryHandler,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_list_query_handler = connection_list_query_handler
        self.connection_service = connection_service

    @ConnectionModels.ns.expect(ConnectionModels.get_connections_parser, validate=True)
    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        """
        Get All Connections
        """

        data = ConnectionModels.get_connections_parser.parse_args(request)
        req: ConnectionListRequest = JsonConvert.FromJSON(json.dumps(data))
        query = ConnectionListQuery(ConnectionListRequest=req)
        res = self.connection_list_query_handler.handle(query=query)
        # result = JsonConvert.ToJSON(res)
        result = json.loads(json.dumps(res.to_dict(), default=CommonModels.date_converter))
        return CommonModels.get_response(result=result)

    @ConnectionModels.ns.expect(ConnectionModels.delete_connection_database_model, validate=True)
    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def delete(self):
        """
        Delete Existing Database Connection
        """
        data = IocManager.api.payload
        id = data.get('Id')  #
        deletion_result = self.connection_service.delete_connection(id)
        return CommonModels.get_response(message="Connection Removed Successfully")
