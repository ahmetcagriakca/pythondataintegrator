from injector import inject

from controllers.connection.models.ConnectionModels import ConnectionModels
from controllers.common.models.CommonModels import CommonModels
from domain.connection.services.ConnectorTypeService import ConnectorTypeService
from infrastructor.api.ResourceBase import ResourceBase


@ConnectionModels.ns.route("/ConnectorType")
class ConnectorTypeResource(ResourceBase):
    @inject
    def __init__(self, connector_type_service: ConnectorTypeService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connector_type_service = connector_type_service

    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        """
        Get Connector Types
        """
        connector_types = self.connector_type_service.get()
        result = ConnectionModels.get_connector_type_models(connector_types)
        return CommonModels.get_response(result=result)

