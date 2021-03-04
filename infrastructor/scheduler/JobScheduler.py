import json
import os
from datetime import datetime, timedelta
from typing import List

import jsonpickle
from apscheduler.triggers.cron import CronTrigger
from flask import jsonify
from apscheduler.events import EVENT_SCHEDULER_STARTED, EVENT_SCHEDULER_SHUTDOWN, EVENT_SCHEDULER_PAUSED, \
    EVENT_SCHEDULER_RESUMED, EVENT_EXECUTOR_ADDED, EVENT_EXECUTOR_REMOVED, EVENT_JOBSTORE_ADDED, EVENT_JOBSTORE_REMOVED, \
    EVENT_ALL_JOBS_REMOVED, EVENT_JOB_ADDED, EVENT_JOB_REMOVED, EVENT_JOB_MODIFIED, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, \
    EVENT_JOB_MISSED, EVENT_JOB_SUBMITTED, EVENT_JOB_MAX_INSTANCES, EVENT_ALL
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.job import Job
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from injector import inject
from pytz import utc
from tzlocal import get_localzone

from infrastructor.IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import ISingleton
from infrastructor.scheduler.JobSchedulerEvent import JobSchedulerEvent
from models.configs.DatabaseConfig import DatabaseConfig
from models.dao.common.ConfigParameter import ConfigParameter


class JobScheduler(ISingleton):
    @inject
    def __init__(self):
        self.scheduler: BackgroundScheduler = None

    def run(self):
        self.run_scheduler()
        print("job_process started")

    def run_scheduler(self):
        
        self.database_session_manager: DatabaseSessionManager = IocManager.injector.get(DatabaseSessionManager)
        self.database_config: DatabaseConfig = IocManager.injector.get(DatabaseConfig)
        jobstores = {
            'default': SQLAlchemyJobStore(url=self.database_config.connection_string, tablename='ApSchedulerJobsTable',
                                          engine=self.database_session_manager.engine,
                                          metadata=IocManager.Base.metadata,
                                          tableschema='Aps')
        }
        executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(10)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 10
        }
        self.scheduler = BackgroundScheduler(daemon=True, jobstores=jobstores, executors=executors,
                                             job_defaults=job_defaults)

        JobSchedulerEvent.job_scheduler_type = JobScheduler
        self.scheduler.add_listener(JobSchedulerEvent.listener_finish, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.scheduler.add_listener(JobSchedulerEvent.listener_job_added, EVENT_JOB_ADDED)
        self.scheduler.add_listener(JobSchedulerEvent.listener_job_submitted, EVENT_JOB_SUBMITTED)
        self.scheduler.add_listener(JobSchedulerEvent.listener_job_removed, EVENT_JOB_REMOVED)
        self.scheduler.add_listener(JobSchedulerEvent.listener_all_jobs_removed, EVENT_ALL_JOBS_REMOVED)
        self.scheduler.add_listener(JobSchedulerEvent.listener_job_others,
                                    EVENT_JOB_MODIFIED | EVENT_JOB_MISSED | EVENT_JOB_MAX_INSTANCES)
        self.scheduler.add_listener(JobSchedulerEvent.listener_scheduler_other_events,
                                    EVENT_SCHEDULER_STARTED | EVENT_SCHEDULER_SHUTDOWN | EVENT_SCHEDULER_PAUSED | EVENT_SCHEDULER_RESUMED | EVENT_EXECUTOR_ADDED | EVENT_EXECUTOR_REMOVED | EVENT_JOBSTORE_ADDED | EVENT_JOBSTORE_REMOVED)
        self.scheduler.start()
        self.scheduler.print_jobs()
        print('To clear the alarms, delete the example.sqlite file.')
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    def add_job_with_date(self, job_function, run_date, args=None, kwargs=None) -> Job:
        # if run_date is None:
        #     run_date = datetime.now() + timedelta(seconds=10)
        job: Job = self.scheduler.add_job(job_function, 'date', run_date=run_date, misfire_grace_time=30000, args=args,
                                          kwargs=kwargs)
        return job

    def add_job_with_cron(self, job_function, cron: CronTrigger, args=None, kwargs=None) -> Job:
        # if cron.start_date is not None and cron.start_date < datetime.now().astimezone(get_localzone()):
        #     cron.start_date = None
        # if cron.end_date is not None and cron.end_date < datetime.now().astimezone(get_localzone()):
        #     cron.end_date = None
        job: Job = self.scheduler.add_job(job_function, cron, misfire_grace_time=15, args=args, kwargs=kwargs)
        return job

    def remove_job(self, job_id):
        self.scheduler.remove_job(job_id)

    def modify_job(self, job_id, jobstore=None, **changes):
        return self.scheduler.modify_job(job_id, jobstore, **changes)

    def reschedule_job(self, job_id, jobstore=None, trigger=None, **trigger_args):
        return self.scheduler.reschedule_job(job_id, jobstore, trigger, **trigger_args)

    def pause_job(self, job_id, jobstore=None):
        return self.scheduler.pause_job(job_id, jobstore)

    def resume_job(self, job_id, jobstore=None):
        return self.scheduler.resume_job(job_id, jobstore)

    def remove_job(self, job_id, jobstore=None):
        self.scheduler.remove_job(job_id, jobstore)

    def get_job(self, job_id):
        return self.scheduler.get_job(job_id)

    def get_jobs(self, jobstore=None):
        return self.scheduler.get_jobs(jobstore)
