from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.job.models.JobModels import JobModels
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.scheduler.JobScheduler import JobScheduler
from models.dao.aps.ApSchedulerJob import ApSchedulerJob


@JobModels.ns.route('/GetJob/<int:job_id>', doc=False)
class GetJobResource(ResourceBase):
    @inject
    def __init__(self,
                 job_scheduler: JobScheduler,
                 database_session_manager: DatabaseSessionManager,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database_session_manager = database_session_manager
        self.ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
            database_session_manager)
        self.job_scheduler: JobScheduler = job_scheduler

    @JobModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self, job_id):
        ap_scheduler_job = self.ap_scheduler_job_repository.get_by_id(job_id)
        if ap_scheduler_job is None:
            return CommonModels.get_error_response(f"Job {job_id} not  found")
        result = JobModels.get_ap_scheduler_job_model(ap_scheduler_job)
        return CommonModels.get_response(result=result)
