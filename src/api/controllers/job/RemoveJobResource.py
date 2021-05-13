from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.job.models.JobModels import JobModels
from IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.scheduler.JobScheduler import JobScheduler
from models.dao.aps.ApSchedulerJob import ApSchedulerJob


@JobModels.ns.route('/RemoveJob', doc=False)
class RemoveJobResource(ResourceBase):
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

    @JobModels.ns.expect(JobModels.RemoveJobModel, validate=True)
    @JobModels.ns.marshal_with(CommonModels.SuccessModel)
    def delete(self):
        data = IocManager.api.payload
        job_id = data.get('JobId')  #
        ap_scheduler_job = self.ap_scheduler_job_repository.filter_by(IsDeleted=0, Id=job_id).first()
        if ap_scheduler_job is None:
            return CommonModels.get_error_response(f"Job {job_id} not found")
        self.job_scheduler.remove_job(job_id=ap_scheduler_job.JobId)
        return CommonModels.get_response(message=f"Job {job_id} removed successfully")
