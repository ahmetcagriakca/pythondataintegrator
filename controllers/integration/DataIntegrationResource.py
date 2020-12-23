import json
from injector import inject

from controllers.common.models.CommonModels import CommonModels
from controllers.integration.models.DataIntegrationModels import DataIntegrationModels
from domain.integration.services.DataIntegrationService import DataIntegrationService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from models.viewmodels.integration.CreateIntegrationDataModel import CreateIntegrationDataModel


@DataIntegrationModels.ns.route("/DataIntegration")
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
        python_data_integrations = self.python_data_integration_repository.filter_by(IsDeleted=0)
        result = DataIntegrationModels.get_pdi_models(python_data_integrations)
        return CommonModels.get_response(result)

    @DataIntegrationModels.ns.expect(DataIntegrationModels.create_integration_data_model, validate=True)
    @DataIntegrationModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Create Integration Data
        """
        data: CreateIntegrationDataModel = json.loads(json.dumps(IocManager.api.payload),
                                                      object_hook=lambda d: CreateIntegrationDataModel(**d))
        creation_result = self.data_integration_service.create_integration_data(data)
        result = DataIntegrationModels.get_pdi_model(creation_result)
        return CommonModels.get_response(result=result)

    @DataIntegrationModels.ns.expect(DataIntegrationModels.delete_integration_data_model, validate=True)
    @DataIntegrationModels.ns.marshal_with(CommonModels.SuccessModel)
    def delete(self):
        """
        Delete Existing Integration Data
        """
        data = IocManager.api.payload
        code = data.get('Code')  #
        deletion_result = self.data_integration_service.delete_integration_data(code)
        return CommonModels.get_response(message=f'PDI deletion for {code} is Completed')

