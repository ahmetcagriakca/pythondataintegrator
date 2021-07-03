from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.connection.models.ConnectionModels import ConnectionModels
from domain.connection.services.ConnectionService import ConnectionService
from IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from rpc.ProcessRpcClientService import ProcessRpcClientService


@ConnectionModels.ns.route("/CheckConnectionDatabase")
class CheckConnectionDatabaseResource(ResourceBase):
    @inject
    def __init__(self, process_rpc_client_service: ProcessRpcClientService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process_rpc_client_service = process_rpc_client_service

    @ConnectionModels.ns.expect(ConnectionModels.check_connection_database_model, validate=True)
    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Check Database Connection
        """
        data = IocManager.api.payload
        name = data.get('Name')  #
        schema = data.get('Schema')  #
        table = data.get('Table')  #
        result = self.process_rpc_client_service.call_check_database_connection(connection_name=name, schema=schema,
                                                                                table=table)

        return CommonModels.get_response(result=result)
