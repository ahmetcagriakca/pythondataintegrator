import json
from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.operation.models.DataOperationModels import DataOperationModels
from domain.operation.services.DataOperationService import DataOperationService
from domain.job.services.JobOperationService import JobOperationService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from models.dao.aps.ApSchedulerJob import ApSchedulerJob
from models.dao.integration.PythonDataIntegration import PythonDataIntegration
from models.dao.integration.PythonDataIntegrationJob import PythonDataIntegrationJob
from models.dao.integration.PythonDataIntegrationLog import PythonDataIntegrationLog
from models.viewmodels.operation.CreateDataOperationModel import CreateDataOperationModel
from models.viewmodels.operation.CreateDataOperationIntegrationModel import CreateDataOperationIntegrationModel
from models.viewmodels.operation.UpdateDataOperationIntegrationModel import UpdateDataOperationIntegrationModel
from models.viewmodels.operation.UpdateDataOperationModel import UpdateDataOperationModel


@DataOperationModels.ns.route("/DataOperation")
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
        Create New Data Operation
        """
        data: CreateDataOperationModel = json.loads(json.dumps(IocManager.api.payload),
                                                    object_hook=lambda d: CreateDataOperationModel(**d))
        data.Integrations = json.loads(json.dumps(IocManager.api.payload["Integrations"]),
                                       object_hook=lambda d: CreateDataOperationIntegrationModel(**d))
        creation_result = self.data_operation_service.create_data_operation(data)
        result = DataOperationModels.get_data_operation_result_model(creation_result)
        return CommonModels.get_response(result=result)

    @DataOperationModels.ns.expect(DataOperationModels.update_data_operation_model, validate=True)
    @DataOperationModels.ns.marshal_with(CommonModels.SuccessModel)
    def put(self):
        """
        Update Existing Data Operation
        """
        data: CreateDataOperationModel = json.loads(json.dumps(IocManager.api.payload),
                                                    object_hook=lambda d: UpdateDataOperationModel(**d))
        data.Integrations = json.loads(json.dumps(IocManager.api.payload["Integrations"]),
                                       object_hook=lambda d: UpdateDataOperationIntegrationModel(**d))
        creation_result = self.data_operation_service.update_data_operation(data)
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


@DataOperationModels.ns.route("/ScheduleJob")
class ScheduleJobResource(ResourceBase):
    @inject
    def __init__(self, data_operation_service: DataOperationService,
                 job_operation_service: JobOperationService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_operation_service = job_operation_service
        self.data_operation_service = data_operation_service

    @DataOperationModels.ns.expect(DataOperationModels.start_operation_model, validate=True)
    @DataOperationModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Start operations
        """
        data = IocManager.api.payload
        operation_name = data.get('OperationName')  #
        run_date = data.get('RunDate')  #
        start_operation_result = self.job_operation_service.add_pdi_job_with_date(operation_name=operation_name, run_date=run_date)
        result = DataOperationModels.get_data_operation_job_model(start_operation_result)
        return CommonModels.get_response(result=result)


@DataOperationModels.ns.route("/ScheduleJobWithCron")
class ScheduleJobWithCronResource(ResourceBase):
    @inject
    def __init__(self, data_operation_service: DataOperationService,
                 job_operation_service: JobOperationService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_operation_service = job_operation_service
        self.data_operation_service = data_operation_service

    @DataOperationModels.ns.expect(DataOperationModels.start_operation_with_cron_model, validate=True)
    @DataOperationModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Start operations
        """
        data = IocManager.api.payload
        operation_name = data.get('OperationName')  #
        cron = data.get('Cron')  #
        start_date = data.get('StartDate')  #
        end_date = data.get('EndDate')  #
        start_operation_result = self.job_operation_service.add_pdi_job_with_cron(operation_name=operation_name, cron=cron,
                                                                                  start_date=start_date,
                                                                                  end_date=end_date)
        result = DataOperationModels.get_data_operation_job_model(start_operation_result)
        return CommonModels.get_response(result=result)

    @DataOperationModels.ns.expect(DataOperationModels.start_operation_with_cron_model,
                                   validate=True)
    @DataOperationModels.ns.marshal_with(CommonModels.SuccessModel)
    def put(self):
        """
        Start operations
        """
        data = IocManager.api.payload
        code = data.get('Code')  #
        cron = data.get('Cron')  #
        start_date = data.get('StartDate')  #
        end_date = data.get('EndDate')  #
        start_operation_result = self.job_operation_service.modify_job(code=code, cron=cron, start_date=start_date,
                                                                       end_date=end_date)
        if isinstance(start_operation_result, PythonDataIntegrationJob):
            result = DataOperationModels.get_data_operation_job_model(start_operation_result)
            return CommonModels.get_response(result=result)
        else:
            message = start_operation_result
            return CommonModels.get_error_response(message=message)


@DataOperationModels.ns.route('/GetJobDetails/<string:code>')
class GetJobDetailsResource(ResourceBase):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database_session_manager = database_session_manager
        self.python_data_integration_log_repository: Repository[PythonDataIntegrationLog] = Repository[
            PythonDataIntegrationLog](
            database_session_manager)

        self.python_data_integration_repository: Repository[PythonDataIntegration] = Repository[PythonDataIntegration](
            database_session_manager)

    @DataOperationModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self, code):
        """
        Job details with code
        """
        python_data_integration = self.python_data_integration_repository.first(Code=code)

        if python_data_integration is None:
            return "Code Not Found"
        result = DataOperationModels.get_data_operation_job_models(python_data_integration.Jobs)
        return CommonModels.get_response(result)


@DataOperationModels.ns.route('/GetJobLogs/<int:job_id>')
class GetJobLogsResource(ResourceBase):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database_session_manager = database_session_manager
        self.python_data_integration_log_repository: Repository[PythonDataIntegrationLog] = Repository[
            PythonDataIntegrationLog](
            database_session_manager)

        self.ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
            database_session_manager)

    @DataOperationModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self, job_id):
        """
        Job logs getting with code
        """
        ap_scheduler_job = self.ap_scheduler_job_repository.first(Id=job_id)
        if ap_scheduler_job is None:
            return "Job Not Found"
        logs = self.python_data_integration_log_repository.filter_by(
            JobId=job_id).all()
        result = DataOperationModels.get_pdi_logs_model(logs)
        return CommonModels.get_response(result)
