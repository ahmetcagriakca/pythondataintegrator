import time
from datetime import datetime

from apscheduler.triggers.cron import CronTrigger
from injector import inject

from domain.operation.services.DataOperationJobService import DataOperationJobService
from domain.operation.services.DataOperationService import DataOperationService
from infrastructor.IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.scheduler.JobScheduler import JobScheduler
from models.dao.aps.ApSchedulerJob import ApSchedulerJob
from models.dao.operation import DataOperation
from models.dao.operation.DataOperationJob import DataOperationJob


class JobOperationService(IScoped):
    data_operation_service: DataOperationService = None

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 data_operation_service: DataOperationService,
                 job_scheduler: JobScheduler
                 ):
        self.data_operation_service = data_operation_service
        self.job_scheduler = job_scheduler
        self.database_session_manager = database_session_manager
        self.data_operation_repository: Repository[DataOperation] = Repository[DataOperation](
            database_session_manager)
        self.data_operation_job_repository: Repository[DataOperationJob] = Repository[DataOperationJob](
            database_session_manager)
        self.ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
            database_session_manager)

        self.sql_logger = sql_logger

    def get_ap_scheduler_with_retry(self, job_id, retry: int = 0) -> ApSchedulerJob:
        ap_scheduler_job = self.ap_scheduler_job_repository.first(JobId=job_id)
        if ap_scheduler_job is None and retry < 3:
            time.sleep(2)
            ap_scheduler_job = self.get_ap_scheduler_with_retry(job_id, retry + 1)
        return ap_scheduler_job

    def modify_job(self, operation_name: str, cron: str, start_date: datetime = None, end_date: datetime = None):
        if cron is None or cron == '':
            raise OperationalException("Cron required")
        data_operation = self.data_operation_repository.first(IsDeleted=0, Name=operation_name)
        if data_operation is None:
            raise OperationalException("Data operation not found")
        data_operation_jobs = self.data_operation_job_repository.filter_by(IsDeleted=0,
                                                                           DataOperationId=data_operation.Id).all()
        if data_operation_jobs is None or len(data_operation_jobs) == 0:
            raise OperationalException("Job not found initialized with cron")
        founded_cron_job: DataOperationJob = None
        for data_operation_job in data_operation_jobs:
            if data_operation_job.Cron is not None:
                founded_cron_job = data_operation_job
                break
        if founded_cron_job is None:
            raise OperationalException("Job not found initialized with cron")
        if start_date is not None and start_date != '':
            job_start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        else:
            job_start_date = datetime.now().astimezone()
        if end_date is not None and end_date != '':
            job_end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        else:
            job_end_date = None
        trigger = CronTrigger.from_crontab(cron)
        trigger.start_date = job_start_date
        trigger.end_date = job_end_date

        for data_operation_job in data_operation_jobs:
            ap_scheduler_job = self.ap_scheduler_job_repository.first(IsDeleted=0,
                                                                      Id=data_operation_job.ApSchedulerJobId)
            try:
                self.job_scheduler.remove_job(job_id=ap_scheduler_job.JobId)
            except Exception as ex:
                pass
        self.data_operation_job_repository.delete_by_id(founded_cron_job.Id)
        ap_scheduler_job = self.add_job_with_cron(job_function=JobOperationService.job_start_data_operation,
                                                  cron=cron, start_date=start_date, end_date=end_date,
                                                  args=(None, data_operation.Id,))

        data_operation_job = self.insert_data_operation_job(ap_scheduler_job, data_operation, cron, start_date,
                                                            end_date)
        return data_operation_job

    def add_job_with_cron(self, job_function, cron, start_date=None, end_date=None, args=None,
                          kwargs=None) -> ApSchedulerJob:

        trigger = CronTrigger.from_crontab(cron)
        trigger.start_date = start_date
        trigger.end_date = end_date
        job = self.job_scheduler.add_job_with_cron(job_function=job_function, cron=trigger, args=args,
                                                   kwargs=kwargs)
        ap_scheduler_job = self.get_ap_scheduler_with_retry(job.id)
        return ap_scheduler_job

    def add_job_with_date(self, job_function, run_date, args=None, kwargs=None) -> ApSchedulerJob:
        job = self.job_scheduler.add_job_with_date(job_function=job_function, run_date=run_date, args=args,
                                                   kwargs=kwargs)
        ap_scheduler_job = self.get_ap_scheduler_with_retry(job.id)
        return ap_scheduler_job

    def insert_data_operation_job(self, ap_scheduler_job, data_operation, cron, start_date, end_date):
        data_operation_job = DataOperationJob(StartDate=start_date, EndDate=end_date,
                                              Cron=cron, ApSchedulerJob=ap_scheduler_job,
                                              DataOperation=data_operation)
        self.data_operation_job_repository.insert(data_operation_job)
        self.database_session_manager.commit()
        return data_operation_job

    #######################################################################################
    def add_pdi_job_with_date(self, operation_name: str, run_date: datetime = None):
        data_operation = self.data_operation_repository.first(IsDeleted=0, Name=operation_name)
        if data_operation is None:
            raise OperationalException("Data operation not found")
        if run_date is not None and run_date != '':
            start_date = datetime.strptime(run_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        else:
            start_date = datetime.now().astimezone()
        ap_scheduler_job = self.add_job_with_date(job_function=JobOperationService.job_start_data_operation,
                                                  run_date=start_date, args=(None, data_operation.Id,))
        data_operation_job = self.insert_data_operation_job(ap_scheduler_job, data_operation, None, start_date, None)
        return data_operation_job

    def check_cron_initialized_jobs(self, data_operation_id):
        data_operation_jobs = self.data_operation_job_repository.filter_by(
            DataOperationId=data_operation_id).all()
        for job in data_operation_jobs:
            if job.Cron is not None and job.IsDeleted == 0:
                raise OperationalException("Job already initialized with cron. ")

    def add_pdi_job_with_cron(self, operation_name: str, cron: str, start_date: datetime = None,
                              end_date: datetime = None):
        if cron is None or cron == '':
            raise OperationalException("Cron required")
        data_operation = self.data_operation_repository.first(IsDeleted=0, Name=operation_name)
        if data_operation is None:
            raise OperationalException("Data Operation not found")

        self.check_cron_initialized_jobs(data_operation.Id)
        if start_date is not None and start_date != '':
            start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        else:
            start_date = datetime.now().astimezone()
        if end_date is not None and end_date != '':
            end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        else:
            end_date = None
        ap_scheduler_job = self.add_job_with_cron(job_function=JobOperationService.job_start_data_operation,
                                                  cron=cron, start_date=start_date, end_date=end_date,
                                                  args=(None, data_operation.Id,))
        data_operation_job = self.insert_data_operation_job(ap_scheduler_job, data_operation, cron, start_date,
                                                            end_date)
        return data_operation_job

    @staticmethod
    def job_start_data_operation(job_id, data_operation_id: int):
        data_operation_job_service: DataOperationJobService = IocManager.injector.get(DataOperationJobService)
        result = data_operation_job_service.start_operation(data_operation_id=data_operation_id, job_id=job_id)
        return result
