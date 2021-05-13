from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.operation.models.DataOperationModels import DataOperationModels
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from models.dao.aps.ApSchedulerJob import ApSchedulerJob
from models.dao.common.Log import Log


@DataOperationModels.ns.route('/GetJobLogs/<int:job_id>', doc=False)
class GetJobLogsResource(ResourceBase):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database_session_manager = database_session_manager
        self.log_repository: Repository[Log] = Repository[Log](
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
        logs = self.log_repository.filter_by(
            JobId=job_id).all()
        result = DataOperationModels.get_pdi_logs_model(logs)
        return CommonModels.get_response(result)
