import json
from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.lookup.models.LookupModels import LookupModels
from domain.connection.services.ConnectionLookupService import ConnectionLookupService
from domain.operation.services.DataOperationLookupService import DataOperationLookupService
from infrastructure.api.ResourceBase import ResourceBase


@LookupModels.ns.route("/DataOperationName")
class DataOperationNameResource(ResourceBase):
    @inject
    def __init__(self,
                 service: DataOperationLookupService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service

    @LookupModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        """
        Get All Data Operations
        """

        res = self.service.get_data_operation_names()
        result = json.loads(json.dumps(res.to_dict(), default=CommonModels.date_converter))
        return CommonModels.get_response(result=result)


