from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.job.models.JobSchedulerModels import JobSchedulerModels
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from models.dao.aps.ApSchedulerJob import ApSchedulerJob


@JobSchedulerModels.ns.route('/GetJobs')
class GetJobsResource(ResourceBase):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database_session_manager = database_session_manager
        self.ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
            database_session_manager)

    @JobSchedulerModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        ap_scheduler_jobs = self.ap_scheduler_job_repository.filter_by(IsDeleted=0).all()
        result = JobSchedulerModels.get_ap_scheduler_job_models(ap_scheduler_jobs)
        return CommonModels.get_response(result=result)

