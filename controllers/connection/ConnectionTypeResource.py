from injector import inject

from controllers.connection.models.ConnectionModels import ConnectionModels
from controllers.common.models.CommonModels import CommonModels
from domain.connection.services.ConnectionService import ConnectionService
from infrastructor.api.ResourceBase import ResourceBase


@ConnectionModels.ns.route("/ConnectionType")
class ConnectionTypeResource(ResourceBase):
    @inject
    def __init__(self, connection_service: ConnectionService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_service = connection_service

    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        """
        Get Connection Types
        """
        connection_types = self.connection_service.get_connection_types()
        result = ConnectionModels.get_connection_type_models(connection_types)
        return CommonModels.get_response(result=result)

