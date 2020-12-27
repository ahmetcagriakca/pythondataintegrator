from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.connection.models.ConnectionModels import ConnectionModels
from domain.connection.services.ConnectionService import ConnectionService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase


@ConnectionModels.ns.route("")
class ConnectionResource(ResourceBase):
    @inject
    def __init__(self, connection_service: ConnectionService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_service = connection_service

    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        """
        Get All Connections
        """
        entities = self.connection_service.get_connections()
        result = ConnectionModels.get_connection_result_models(entities)
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


