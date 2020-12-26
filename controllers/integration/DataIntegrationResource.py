import json
from injector import inject

from controllers.common.models.CommonModels import CommonModels
from controllers.integration.models.DataIntegrationModels import DataIntegrationModels
from domain.integration.services.DataIntegrationService import DataIntegrationService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from models.viewmodels.integration.CreateDataIntegrationModel import CreateDataIntegrationModel


@DataIntegrationModels.ns.route("")
class DataIntegrationResource(ResourceBase):
    @inject
    def __init__(self,
                 data_integration_service: DataIntegrationService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_integration_service = data_integration_service

    @DataIntegrationModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        """
        All integration data
        """
        data_integrations = self.data_integration_service.get_data_integrations()
        result = DataIntegrationModels.get_data_integration_models(data_integrations)
        return CommonModels.get_response(result)

    @DataIntegrationModels.ns.expect(DataIntegrationModels.create_data_integration_model, validate=True)
    @DataIntegrationModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Create Integration Data
        """
        data: CreateDataIntegrationModel = json.loads(json.dumps(IocManager.api.payload),
                                                      object_hook=lambda d: CreateDataIntegrationModel(**d))
        data_integrations = self.data_integration_service.create_data_integration(data)
        result = DataIntegrationModels.get_data_integration_model(data_integrations)
        return CommonModels.get_response(result=result)

    @DataIntegrationModels.ns.expect(DataIntegrationModels.delete_data_integration_model, validate=True)
    @DataIntegrationModels.ns.marshal_with(CommonModels.SuccessModel)
    def delete(self):
        """
        Delete Existing Integration Data
        """
        data = IocManager.api.payload
        code = data.get('Code')  #
        deletion_result = self.data_integration_service.delete_integration_data(code)
        return CommonModels.get_response(message=f'PDI deletion for {code} is Completed')

