from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.job.models.JobSchedulerModels import JobSchedulerModels
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.scheduler.JobScheduler import JobScheduler
from models.dao.aps import ApSchedulerJobEvent


@JobSchedulerModels.ns.route('/GetJobEvents/<int:job_id>')
class GetJobEvents(ResourceBase):
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
