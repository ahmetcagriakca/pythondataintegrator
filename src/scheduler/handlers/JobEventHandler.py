import traceback
from queue import Queue

from injector import inject

from domain.operation.services.DataOperationJobService import DataOperationJobService
from IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped

from apscheduler.events import EVENT_JOB_MISSED

from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.utils.Utils import Utils
from models.dao.aps import ApSchedulerJob, ApSchedulerJobEvent, ApSchedulerEvent
from models.dao.operation import DataOperationJob


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
        self.ap_scheduler_event_repository: Repository[ApSchedulerEvent] = Repository[ApSchedulerEvent](
            database_session_manager)
        self.ap_scheduler_job_event_repository: Repository[ApSchedulerJobEvent] = Repository[ApSchedulerJobEvent](
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
                if event.code == EVENT_JOB_MISSED:
                    self.missed_job(job_id=event.job_id)

            except Exception as ex:
                self.sql_logger.error(f"Job event getting error. Error:{ex}- Traceback:{traceback.format_exc()}")

    def job_transaction_handler(func):
        def inner(*args, **kwargs):
            try:
                args[0].database_session_manager.close()
                args[0].database_session_manager.connect()
                result = func(*args, **kwargs)
                args[0].database_session_manager.commit()
                return result
            except Exception as ex:
                try:
                    args[0].database_session_manager.rollback()
                    args[0].database_session_manager.close()
                    args[0].database_session_manager.connect()
                    result = func(*args, **kwargs)
                    args[0].database_session_manager.commit()
                    return result
                except Exception as invalid_ex:
                    print(ex)
                    raise

        return inner

    @job_transaction_handler
    def missed_job(self, job_id):
        ap_scheduler_job = self.ap_scheduler_job_repository.first(JobId=job_id)
        self.data_operation_job_service.send_data_operation_miss_mail(ap_scheduler_job=ap_scheduler_job)
