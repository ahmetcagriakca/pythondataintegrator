from typing import List
import jsonpickle
from apscheduler.job import Job
from injector import inject
from infrastructor.IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import ISingleton
from infrastructor.logging.SqlLogger import SqlLogger
from models.dao.aps.ApSchedulerEvent import ApSchedulerEvent
from models.dao.aps.ApSchedulerJob import ApSchedulerJob
from models.dao.aps.ApSchedulerJobEvent import ApSchedulerJobEvent


class JobSchedulerEvent(ISingleton):
    job_scheduler_type = None

    @inject
    def __init__(self):
        pass

    @staticmethod
    def get_job(job_id) -> Job:
        job_scheduler = IocManager.injector.get(JobSchedulerEvent.job_scheduler_type)
        job: Job = job_scheduler.scheduler.get_job(job_id)
        return job

    @staticmethod
    def add_log(event, log_text):
        sql_logger = IocManager.injector.get(SqlLogger)
        database_session_manager = IocManager.injector.get(DatabaseSessionManager)
        ap_scheduler_event_repository: Repository[ApSchedulerEvent] = Repository[ApSchedulerEvent](
            database_session_manager)
        ap_scheduler_event: ApSchedulerEvent = ap_scheduler_event_repository.first(Code=event.code)
        job_detail = ''
        job_id = None
        if hasattr(event, 'job_id') and event.job_id:
            ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
                database_session_manager)
            ap_scheduler_job: List[ApSchedulerJob] = ap_scheduler_job_repository.first(JobId=event.job_id)
            job_id = ap_scheduler_job.Id
            job_detail = f'job_id:{job_id} - evennt_job_id:{event.job_id}  - job_store:{event.jobstore} - '

        if hasattr(event, 'exception') and event.exception:
            sql_logger.error(f'{job_detail}{ap_scheduler_event.Name} - {log_text}', job_id=job_id)
        else:
            sql_logger.info(f'{job_detail}{ap_scheduler_event.Name} - {log_text}', job_id=job_id)

    @staticmethod
    def add_job(event):
        job = JobSchedulerEvent.get_job(event.job_id)

        database_session_manager = IocManager.injector.get(DatabaseSessionManager)
        ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
            database_session_manager)
        ap_scheduler_job = ApSchedulerJob(JobId=job.id, NextRunTime=job.next_run_time, FuncRef=job.func_ref)
        ap_scheduler_job_repository.insert(ap_scheduler_job)
        database_session_manager.commit()
        job_args = (ap_scheduler_job.Id,)+job.args[1:]
        job.modify(args=job_args)

    @staticmethod
    def update_job(event):
        job = JobSchedulerEvent.get_job(event.job_id)
        database_session_manager: DatabaseSessionManager = IocManager.injector.get(DatabaseSessionManager)
        ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
            database_session_manager)
        ap_scheduler_job: List[ApSchedulerJob] = ap_scheduler_job_repository.first(JobId=event.job_id)
        if ap_scheduler_job is None:
            job.remove()
        if hasattr(job, 'next_run_time') and job.next_run_time:
            ap_scheduler_job.NextRunTime = job.next_run_time
        else:
            ap_scheduler_job.NextRunTime = None
        database_session_manager.commit()

    @staticmethod
    def remove_job(event):
        database_session_manager: DatabaseSessionManager = IocManager.injector.get(DatabaseSessionManager)
        ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
            database_session_manager)
        ap_scheduler_job: List[ApSchedulerJob] = ap_scheduler_job_repository.first(JobId=event.job_id)
        ap_scheduler_job.IsDeleted = 1
        database_session_manager.commit()

    @staticmethod
    def add_job_event(event):
        database_session_manager = IocManager.injector.get(DatabaseSessionManager)
        ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
            database_session_manager)
        ap_scheduler_event_repository: Repository[ApSchedulerEvent] = Repository[ApSchedulerEvent](
            database_session_manager)
        ap_scheduler_job_event_repository: Repository[ApSchedulerJobEvent] = Repository[ApSchedulerJobEvent](
            database_session_manager)
        ap_scheduler_job = ap_scheduler_job_repository.first(JobId=event.job_id)
        ap_scheduler_event = ap_scheduler_event_repository.first(Code=event.code)
        ap_scheduler_job_event = ApSchedulerJobEvent(ApSchedulerEvent=ap_scheduler_event,
                                                     ApSchedulerJob=ap_scheduler_job)
        ap_scheduler_job_event_repository.insert(ap_scheduler_job_event)
        database_session_manager.commit()

    @staticmethod
    def listener_job_added(event, *args, **kwargs):
        job = JobSchedulerEvent.get_job(event.job_id)
        JobSchedulerEvent.add_job(event)
        JobSchedulerEvent.add_job_event(event)
        JobSchedulerEvent.add_log(event,
                                  f'{job.name} added with funct_ref:{job.func_ref}, max_instances:{job.max_instances}')

    @staticmethod
    def listener_job_removed(event, *args, **kwargs):
        JobSchedulerEvent.add_job_event(event)
        JobSchedulerEvent.remove_job(event)
        JobSchedulerEvent.add_log(event, f'Job removed')

    @staticmethod
    def listener_all_jobs_removed(event, *args, **kwargs):
        JobSchedulerEvent.add_job_event(event)
        JobSchedulerEvent.remove_job(event)
        JobSchedulerEvent.add_log(event, f'Jobs removed')

    @staticmethod
    def listener_finish(event, *args, **kwargs):
        JobSchedulerEvent.add_job_event(event)
        if hasattr(event, 'exception') and event.exception:
            if hasattr(event, 'traceback') and event.traceback:
                JobSchedulerEvent.add_log(event, f'exception:{event.exception} traceback:{event.traceback}')
            else:
                JobSchedulerEvent.add_log(event, f'exception:{event.exception}')
        else:
            retval = None
            if hasattr(event, 'retval') and event.retval:
                retval = event.retval
            retval_string = jsonpickle.encode(retval)
            JobSchedulerEvent.add_log(event, f'return value:{retval_string}')

    @staticmethod
    def listener_job_submitted(event, *args, **kwargs):
        job = JobSchedulerEvent.get_job(event.job_id)
        next_run_time = None
        if hasattr(job, 'next_run_time') and job.next_run_time:
            next_run_time = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        JobSchedulerEvent.add_job_event(event)
        JobSchedulerEvent.update_job(event)
        JobSchedulerEvent.add_log(event, f'Next Run Time:{next_run_time}')

    @staticmethod
    def listener_job_others(event, *args, **kwargs):
        JobSchedulerEvent.add_job_event(event)
        JobSchedulerEvent.add_log(event, f'')

    @staticmethod
    def listener_scheduler_other_events(event, *args, **kwargs):
        JobSchedulerEvent.add_log(event, f'')
