import time
from datetime import datetime
from typing import List

from apscheduler.triggers.cron import CronTrigger
from injector import inject

from domain.pdi.services.DataOperationService import DataOperationService
from infrastructor.IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.scheduler.JobScheduler import JobScheduler
from models.dao.aps.ApSchedulerJob import ApSchedulerJob
from models.dao.integration.PythonDataIntegrationJob import PythonDataIntegrationJob
from models.dao.integration.PythonDataIntegration import PythonDataIntegration


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
        self.python_data_integration_repository: Repository[PythonDataIntegration] = Repository[PythonDataIntegration](
            database_session_manager)
        self.python_data_integration_job_repository: Repository[PythonDataIntegrationJob] = Repository[
            PythonDataIntegrationJob](database_session_manager)
        self.ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
            database_session_manager)

        self.sql_logger = sql_logger

    def get_ap_scheduler_with_retry(self, job_id, retry: int = 0) -> ApSchedulerJob:
        ap_scheduler_job = self.ap_scheduler_job_repository.first(JobId=job_id)
        if ap_scheduler_job is None and retry < 3:
            time.sleep(2)
            ap_scheduler_job = self.get_ap_scheduler_with_retry(job_id, retry + 1)
        return ap_scheduler_job

    def modify_job(self, code: str, cron: str, start_date: datetime = None, end_date: datetime = None):
        if cron is None or cron == '':
            raise OperationalException("Cron required")
        pdi = self.python_data_integration_repository.first(IsDeleted=0, Code=code)
        if pdi is None:
            raise OperationalException("Code Not Found")
        pdi_jobs = self.python_data_integration_job_repository.filter_by(IsDeleted=0,
                                                                         PythonDataIntegrationId=pdi.Id).all()
        if pdi_jobs is None or len(pdi_jobs) == 0:
            raise OperationalException("Job not found initialized with cron")
        founded_cron_job: PythonDataIntegrationJob = None
        for pdi_job in pdi_jobs:
            if pdi_job.Cron is not None:
                founded_cron_job = pdi_job
                break
        if founded_cron_job is None:
            raise OperationalException("Job not found initialized with cron")
        if start_date is not None or start_date != '':
            start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        if end_date is not None or end_date != '':
            end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        trigger = CronTrigger.from_crontab(cron)
        trigger.start_date = start_date
        trigger.end_date = end_date
        if founded_cron_job.ApSchedulerJob.IsDeleted == 0:
            self.job_scheduler.remove_job(job_id=founded_cron_job.ApSchedulerJob.JobId)
        self.python_data_integration_job_repository.delete_by_id(founded_cron_job.Id)
        ap_scheduler_job = self.add_job_with_cron(job_function=JobOperationService.job_pdi_start_operation,
                                                  cron=cron, start_date=start_date, end_date=end_date,
                                                  args=(None, code,))

        python_data_integration_job = self.insert_pdi_job(ap_scheduler_job, pdi, cron, start_date, end_date)
        return python_data_integration_job

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

    def insert_pdi_job(self, ap_scheduler_job, pdi, cron, start_date, end_date):
        python_data_integration_job = PythonDataIntegrationJob(StartDate=start_date, EndDate=end_date,
                                                               Cron=cron, ApSchedulerJob=ap_scheduler_job,
                                                               PythonDataIntegration=pdi)
        self.python_data_integration_job_repository.insert(python_data_integration_job)
        self.database_session_manager.commit()
        return python_data_integration_job

    #######################################################################################
    def add_pdi_job_with_date(self, code: str, run_date: datetime = None):
        pdi = self.python_data_integration_repository.first(IsDeleted=0, Code=code)
        if pdi is None:
            raise OperationalException("Code Not Found")
        if run_date is not None or run_date != '':
            start_date = datetime.strptime(run_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        else:
            start_date = datetime.now().astimezone()
        ap_scheduler_job = self.add_job_with_date(job_function=JobOperationService.job_pdi_start_operation,
                                                  run_date=start_date, args=(None, code,))
        python_data_integration_job = self.insert_pdi_job(ap_scheduler_job, pdi, None, start_date, None)
        return python_data_integration_job

    def add_pdi_job_with_cron(self, code: str, cron: str, start_date: datetime = None, end_date: datetime = None):
        if cron is None or cron == '':
            raise OperationalException("Cron required")
        pdi = self.python_data_integration_repository.first(IsDeleted=0, Code=code)
        if pdi is None:
            raise OperationalException("Code Not Found")
        pdi_jobs = self.python_data_integration_job_repository.filter_by(
            PythonDataIntegrationId=pdi.Id).all()
        for pdi_job in pdi_jobs:
            if pdi_job.Cron is not None and pdi_job.IsDeleted == 0:
                raise OperationalException("Job already initialized with cron")

        if start_date is not None or start_date != '':
            start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        if end_date is not None or end_date != '':
            end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        ap_scheduler_job = self.add_job_with_cron(job_function=JobOperationService.job_pdi_start_operation,
                                                  cron=cron, start_date=start_date, end_date=end_date,
                                                  args=(None, code,))
        python_data_integration_job = self.insert_pdi_job(ap_scheduler_job, pdi, cron, start_date, end_date)
        return python_data_integration_job

    @staticmethod
    def job_pdi_start_operation(job_id, code: str):
        data_operation_service: DataOperationService = IocManager.injector.get(DataOperationService)
        job_scheduler: JobScheduler = IocManager.injector.get(JobScheduler)

        database_session_manager: DatabaseSessionManager = IocManager.injector.get(DatabaseSessionManager)
        python_data_integration_repository: Repository[PythonDataIntegration] = Repository[PythonDataIntegration](
            database_session_manager)
        python_data_integration_job_repository: Repository[PythonDataIntegrationJob] = Repository[
            PythonDataIntegrationJob](
            database_session_manager)
        pdis: List[PythonDataIntegration] = python_data_integration_repository.filter_by(Code=code).all()
        founded_pdi: PythonDataIntegration = None
        if pdis is not None and len(pdis) > 0:
            for pdi in pdis:
                if pdi.IsDeleted == 0:
                    founded_pdi = pdi
        if founded_pdi is None:
            for pdi in pdis:
                if pdi.IsDeleted == 1:
                    founded_jobs = python_data_integration_job_repository.filter_by(
                        PythonDataIntegrationId=pdi.Id).all()
                    for founded_job in founded_jobs:
                        job_scheduler.scheduler.remove_job(job_id=founded_job.ApSchedulerJob.JobId)
                        return
        founded_job = python_data_integration_job_repository.first(PythonDataIntegrationId=founded_pdi.Id,
                                                                   ApSchedulerJobId=job_id)
        if founded_job is not None and founded_job.IsDeleted == 1:
            job_scheduler.scheduler.remove_job(job_id=founded_job.ApSchedulerJob.JobId)
            return

        data_operation_service.start_operation(code, job_id=job_id)
        return "Operation Completed"
