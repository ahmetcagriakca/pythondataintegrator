from queue import Queue

from injector import inject

from domain.operation.services.DataOperationJobService import DataOperationJobService
from infrastructor.IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped

from apscheduler.events import EVENT_SCHEDULER_STARTED, EVENT_SCHEDULER_SHUTDOWN, EVENT_SCHEDULER_PAUSED, \
    EVENT_SCHEDULER_RESUMED, EVENT_EXECUTOR_ADDED, EVENT_EXECUTOR_REMOVED, EVENT_JOBSTORE_ADDED, EVENT_JOBSTORE_REMOVED, \
    EVENT_ALL_JOBS_REMOVED, EVENT_JOB_ADDED, EVENT_JOB_REMOVED, EVENT_JOB_MODIFIED, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, \
    EVENT_JOB_MISSED, EVENT_JOB_SUBMITTED, EVENT_JOB_MAX_INSTANCES

from infrastructor.logging.SqlLogger import SqlLogger
from models.dao.aps import ApSchedulerJob


class JobEventHandler(IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 data_operation_job_service: DataOperationJobService,
                 database_session_manager: DatabaseSessionManager):
        self.sql_logger = sql_logger
        self.data_operation_job_service = data_operation_job_service
        self.database_session_manager = database_session_manager
        self.ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
            database_session_manager)

    @staticmethod
    def start_job_event_handler_process(sub_process_id,
                                        event_queue: Queue) -> int:
        return IocManager.injector.get(JobEventHandler).start_job_event_handler(
            event_queue=event_queue
        )

    def start_job_event_handler(self, event_queue: Queue):
        while True:
            event = event_queue.get()
            try:
                # if event.code == EVENT_JOB_REMOVED:
                #     self.remove_job(job_id=event.job_id)
                # el
                if event.code == EVENT_JOB_MISSED:
                    self.missed_job(job_id=event.job_id)
            except Exception as ex:
                self.sql_logger.error(f"Job event getting error. Error:{ex}")

    def remove_job(self, job_id):
        ap_scheduler_job = self.ap_scheduler_job_repository.first(JobId=job_id)
        self.data_operation_job_service.remove_data_operation_job(ap_scheduler_job_id=ap_scheduler_job.Id)
        self.database_session_manager.commit()

    def missed_job(self, job_id):
        ap_scheduler_job = self.ap_scheduler_job_repository.first(JobId=job_id)
        self.data_operation_job_service.send_data_operation_miss_mail(ap_scheduler_job=ap_scheduler_job)
        self.database_session_manager.commit()
