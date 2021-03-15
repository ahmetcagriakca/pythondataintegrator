import json
from infrastructor.json.JsonConvert import JsonConvert

from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.operation.models.DataOperationModels import DataOperationModels
from domain.operation.services.DataOperationService import DataOperationService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from models.viewmodels.operation.CreateDataOperationModel import CreateDataOperationModel


@DataOperationModels.ns.route("")
class DataOperationResource(ResourceBase):
    @inject
    def __init__(self, data_operation_service: DataOperationService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_operation_service = data_operation_service

    @DataOperationModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        """
        Get All Data Operations
        """
        entities = self.data_operation_service.get_data_operations()
        result = DataOperationModels.get_data_operation_result_models(entities)
        return CommonModels.get_response(result=result)

    @DataOperationModels.ns.expect(DataOperationModels.create_data_operation_model, validate=True)
    @DataOperationModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Data Operation definition
        """
        data: CreateDataOperationModel = JsonConvert.FromJSON(json.dumps(IocManager.api.payload))
        creation_result = self.data_operation_service.post_data_operation(
            data_operation_model=data,
            definition_json=JsonConvert.ToJSON(data))
        result = DataOperationModels.get_data_operation_result_model(creation_result)
        return CommonModels.get_response(result=result)

    @DataOperationModels.ns.expect(DataOperationModels.delete_data_operation_model, validate=True)
    @DataOperationModels.ns.marshal_with(CommonModels.SuccessModel)
    def delete(self):
        """
        Delete Existing Data Operation
        """
        data = IocManager.api.payload
        id = data.get('Id')  #
        deletion_result = self.data_operation_service.delete_data_operation(id)
        return CommonModels.get_response(message="Data Operation removed successfully")
