import json
from injector import inject

from controllers.models.CommonModels import CommonModels
from controllers.models.PythonDataIntegrationModels import PythonDataIntegrationModels
from domain.pdi.services.ConfigurationOperationService import ConfigurationOperationService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from models.dao.integration.PythonDataIntegration import PythonDataIntegration
from models.dao.integration.PythonDataIntegrationLog import PythonDataIntegrationLog
from models.viewmodels.CreateIntegrationDataModel import CreateIntegrationDataModel

@PythonDataIntegrationModels.ns.route("/IntegrationData")
class CreateIntegrationDataResource(ResourceBase):
    @inject
    def __init__(self,
                 configuration_operation_service: ConfigurationOperationService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configuration_operation_service = configuration_operation_service

    @PythonDataIntegrationModels.ns.expect(PythonDataIntegrationModels.create_integration_data_model, validate=True)
    @PythonDataIntegrationModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Create Integration Data
        """
        data: CreateIntegrationDataModel = json.loads(json.dumps(IocManager.api.payload),
                                                      object_hook=lambda d: CreateIntegrationDataModel(**d))
        creation_result = self.configuration_operation_service.create_integration_data(data)
        result = PythonDataIntegrationModels.get_pdi_model(creation_result)
        return CommonModels.get_response(result=result)

    @PythonDataIntegrationModels.ns.expect(PythonDataIntegrationModels.delete_integration_data_model, validate=True)
    @PythonDataIntegrationModels.ns.marshal_with(CommonModels.SuccessModel)
    def delete(self):
        """
        Delete Existing Integration Data
        """
        data = IocManager.api.payload
        code = data.get('Code')  #
        deletion_result = self.configuration_operation_service.delete_integration_data(code)
        return CommonModels.get_response(message=f'PDI deletion for {code} is Completed')


@PythonDataIntegrationModels.ns.route('/GetAllIntegrationData')
class GetAllIntegrationDataResource(ResourceBase):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database_session_manager = database_session_manager
        self.python_data_integration_log_repository: Repository[PythonDataIntegrationLog] = Repository[
            PythonDataIntegrationLog](database_session_manager)

        self.python_data_integration_repository: Repository[PythonDataIntegration] = Repository[PythonDataIntegration](
            database_session_manager)

    @PythonDataIntegrationModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        """
        All integration data
        """
        python_data_integrations = self.python_data_integration_repository.filter_by(IsDeleted=0)
        result = PythonDataIntegrationModels.get_pdi_models(python_data_integrations)
        return CommonModels.get_response(result)

