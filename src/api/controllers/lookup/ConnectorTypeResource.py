import json

from injector import inject

from controllers.common.models.CommonModels import CommonModels
from controllers.lookup.models.LookupModels import LookupModels
from domain.connection.services.ConnectionLookupService import ConnectionLookupService
from infrastructor.api.ResourceBase import ResourceBase


@LookupModels.ns.route("/ConnectorType")
class ConnectorTypeResource(ResourceBase):
    @inject
    def __init__(self,
                 service: ConnectionLookupService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service

    @LookupModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        """
        Get All Connector Types
        """

        res = self.service.get_connector_type_names()
        result = json.loads(json.dumps(res.to_dict(), default=CommonModels.date_converter))
        return CommonModels.get_response(result=result)