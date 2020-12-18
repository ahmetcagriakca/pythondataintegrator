from injector import inject
from controllers.models.CommonModels import CommonModels
from controllers.models.JobSchedulerModels import JobSchedulerModels
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.scheduler.JobScheduler import JobScheduler
from models.dao.aps.ApSchedulerJob import ApSchedulerJob
from models.dao.aps.ApSchedulerJobEvent import ApSchedulerJobEvent


@JobSchedulerModels.ns.route('/RemoveJob')
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

    @JobSchedulerModels.ns.expect(JobSchedulerModels.RemoveJobModel, validate=True)
    @JobSchedulerModels.ns.marshal_with(CommonModels.SuccessModel)
    def delete(self):
        data = IocManager.api.payload
        job_id = data.get('JobId')  #
        ap_scheduler_job = self.ap_scheduler_job_repository.filter_by(IsDeleted=0, Id=job_id).first()
        if ap_scheduler_job is None:
            return CommonModels.get_error_response(f"Job {job_id} not found")
        self.job_scheduler.remove_job(job_id=ap_scheduler_job.JobId)
        return CommonModels.get_response(message=f"Job {job_id} removed successfully")


@JobSchedulerModels.ns.route('/GetJob/<int:job_id>')
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

    @JobSchedulerModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self, job_id):
        ap_scheduler_job = self.ap_scheduler_job_repository.get_by_id(job_id)
        if ap_scheduler_job is None:
            return CommonModels.get_error_response(f"Job {job_id} not  found")
        result = JobSchedulerModels.get_ap_scheduler_job_model(ap_scheduler_job)
        return CommonModels.get_response(result=result)


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


@JobSchedulerModels.ns.route('/GetJobEvents/<int:job_id>')
class TestResource(ResourceBase):
    @inject
    def __init__(self,
                 job_scheduler: JobScheduler,
                 database_session_manager: DatabaseSessionManager,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database_session_manager = database_session_manager
        self.ap_scheduler_job_event_repository: Repository[ApSchedulerJobEvent] = Repository[ApSchedulerJobEvent](
            database_session_manager)

    @JobSchedulerModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self, job_id):
        ap_scheduler_job_events = self.ap_scheduler_job_event_repository.filter_by(ApSchedulerJobId=job_id).all()
        result = JobSchedulerModels.get_ap_scheduler_job_events_model(ap_scheduler_job_events)
        return CommonModels.get_response(result)
