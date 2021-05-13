from queue import Queue
from typing import List
from apscheduler.job import Job

from IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.logging.SqlLogger import SqlLogger
from models.configs.DatabaseConfig import DatabaseConfig
from models.dao.aps import ApSchedulerJobEvent
from models.dao.aps.ApSchedulerEvent import ApSchedulerEvent
from models.dao.aps.ApSchedulerJob import ApSchedulerJob


class JobSchedulerService:
    def __init__(self,
                 ):

        self.sql_logger = SqlLogger()
        database_config = IocManager.config_manager.get(DatabaseConfig)
        self.database_session_manager = DatabaseSessionManager(database_config=database_config)
        self.ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
            self.database_session_manager)
        self.ap_scheduler_event_repository: Repository[ApSchedulerEvent] = Repository[ApSchedulerEvent](
            self.database_session_manager)
        self.ap_scheduler_job_event_repository: Repository[ApSchedulerJobEvent] = Repository[ApSchedulerJobEvent](
            self.database_session_manager)
        self.job_scheduler_type = None
        self.job_event_queue: Queue = None

    # handle transaction and handle unexpected errors
    def job_transaction_handler(func):
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                args[0].database_session_manager.commit()
                return result
            except Exception as ex:
                try:
                    args[0].database_session_manager.rollback()
                    args[0].database_session_manager.connect()
                    return func(*args, **kwargs)
                except Exception as invalid_ex:
                    print(ex)
                    raise

        return inner

    def set_job_scheduler_type(self, job_scheduler_type):
        self.job_scheduler_type = job_scheduler_type

    def set_job_event_queue(self, job_event_queue: Queue):
        self.job_event_queue = job_event_queue

    def get_job_scheduler(self):
        job_scheduler = IocManager.injector.get(self.job_scheduler_type)
        return job_scheduler

    def get_job(self, job_id) -> Job:
        job_scheduler = self.get_job_scheduler()
        job: Job = job_scheduler.get_job(job_id)
        return job

    @job_transaction_handler
    def add_log(self, event, log_text):
        ap_scheduler_event: ApSchedulerEvent = self.ap_scheduler_event_repository.first(Code=event.code)
        job_detail = ''
        if hasattr(event, 'job_id') and event.job_id:
            ap_scheduler_job: List[ApSchedulerJob] = self.ap_scheduler_job_repository.first(JobId=event.job_id)
            job_id = ''
            if ap_scheduler_job is not None:
                job_id = ap_scheduler_job.Id
            job_detail = f'job_id:{job_id} - event_job_id:{event.job_id}  - job_store:{event.jobstore} - '

        if hasattr(event, 'exception') and event.exception:
            self.sql_logger.error(f'{job_detail}{ap_scheduler_event.Name} - {log_text}')
        else:
            self.sql_logger.info(f'{job_detail}{ap_scheduler_event.Name} - {log_text}')

    @job_transaction_handler
    def add_job(self, event):
        job = self.get_job(event.job_id)

        ap_scheduler_job = ApSchedulerJob(JobId=job.id, NextRunTime=job.next_run_time, FuncRef=job.func_ref)
        self.ap_scheduler_job_repository.insert(ap_scheduler_job)
        self.database_session_manager.commit()
        job_args = (ap_scheduler_job.Id,) + job.args[1:]
        job.modify(args=job_args)

    @job_transaction_handler
    def update_job(self, event):
        job = self.get_job(event.job_id)
        ap_scheduler_job: List[ApSchedulerJob] = self.ap_scheduler_job_repository.first(JobId=event.job_id)
        if ap_scheduler_job is None:
            job.remove()
        if hasattr(job, 'next_run_time') and job.next_run_time:
            ap_scheduler_job.NextRunTime = job.next_run_time
        else:
            ap_scheduler_job.NextRunTime = None

    @job_transaction_handler
    def remove_job(self, event):
        ap_scheduler_job: ApSchedulerJob = self.ap_scheduler_job_repository.first(JobId=event.job_id)
        if ap_scheduler_job is not None:
            self.ap_scheduler_job_repository.delete(ap_scheduler_job)

    @job_transaction_handler
    def add_job_event(self, event):
        ap_scheduler_job = self.ap_scheduler_job_repository.first(JobId=event.job_id)
        ap_scheduler_event = self.ap_scheduler_event_repository.first(Code=event.code)
        ap_scheduler_job_event = ApSchedulerJobEvent(ApSchedulerEvent=ap_scheduler_event,
                                                     ApSchedulerJob=ap_scheduler_job)
        self.ap_scheduler_job_event_repository.insert(ap_scheduler_job_event)
        self.job_event_queue.put(event, timeout=30)
