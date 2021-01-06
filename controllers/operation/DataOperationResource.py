import json
from typing import List

from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.operation.models.DataOperationModels import DataOperationModels
from domain.operation.services.DataOperationService import DataOperationService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from models.viewmodels.integration.CreateDataIntegrationModel import CreateDataIntegrationModel
from models.viewmodels.integration.UpdateDataIntegrationModel import UpdateDataIntegrationModel
from models.viewmodels.operation.CreateDataOperationModel import CreateDataOperationModel
from models.viewmodels.operation.CreateDataOperationIntegrationModel import CreateDataOperationIntegrationModel
from models.viewmodels.operation.UpdateDataOperationIntegrationModel import UpdateDataOperationIntegrationModel
from models.viewmodels.operation.UpdateDataOperationModel import UpdateDataOperationModel


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
        data: CreateDataOperationModel = json.loads(json.dumps(IocManager.api.payload),
                                                    object_hook=lambda d: CreateDataOperationModel(**d))
        data_operation_integrations: List[CreateDataOperationIntegrationModel] = []
        data_operation_integration: CreateDataOperationIntegrationModel = None
        for data_integration in IocManager.api.payload["Integrations"]:
            data_operation_integration = CreateDataOperationIntegrationModel()
            data_operation_integration.Limit = data_integration["Limit"]
            data_operation_integration.ProcessCount = data_integration["ProcessCount"]
            data_operation_integration.Integration = json.loads(json.dumps(data_integration["Integration"]),
                                                                object_hook=lambda d: CreateDataIntegrationModel(**d))
            data_operation_integrations.append(data_operation_integration)
        data.Integrations = data_operation_integrations
        creation_result = self.data_operation_service.post_data_operation(data)
        result = DataOperationModels.get_data_operation_result_model(creation_result)
        return CommonModels.get_response(result=result)

    # @DataOperationModels.ns.expect(DataOperationModels.update_data_operation_model, validate=True)
    # @DataOperationModels.ns.marshal_with(CommonModels.SuccessModel)
    # def put(self):
    #     """
    #     Update Existing Data Operation
    #     """
    #     data: CreateDataOperationModel = json.loads(json.dumps(IocManager.api.payload),
    #                                                 object_hook=lambda d: UpdateDataOperationModel(**d))
    #     data_operation_integrations: List[CreateDataOperationIntegrationModel] = []
    #     data_operation_integration: CreateDataOperationIntegrationModel = None
    #     for data_integration in IocManager.api.payload["Integrations"]:
    #         data_operation_integration = CreateDataOperationIntegrationModel()
    #         data_operation_integration.Limit = data_integration["Limit"]
    #         data_operation_integration.ProcessCount = data_integration["ProcessCount"]
    #         data_operation_integration.Integration = json.loads(json.dumps(data_integration["Integration"]),
    #                                                             object_hook=lambda d: UpdateDataIntegrationModel(**d))
    #         data_operation_integrations.append(data_operation_integration)
    #     data.Integrations = data_operation_integrations
    #     # data: CreateDataOperationModel = json.loads(json.dumps(IocManager.api.payload),
    #     #                                             object_hook=lambda d: UpdateDataOperationModel(**d))
    #     # data.Integrations = json.loads(json.dumps(IocManager.api.payload["Integrations"]),
    #     #                                object_hook=lambda d: UpdateDataOperationIntegrationModel(**d))
    #     creation_result = self.data_operation_service.update_data_operation(data)
    #     result = DataOperationModels.get_data_operation_result_model(creation_result)
    #     return CommonModels.get_response(result=result)

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
