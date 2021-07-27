import time
from datetime import datetime
from typing import List
from injector import inject

from infrastructure.data.RepositoryProvider import RepositoryProvider
from rpc.SchedulerRpcClientService import SchedulerRpcClientService
from domain.operation.services.DataOperationJobService import DataOperationJobService
from domain.operation.services.DataOperationService import DataOperationService
from infrastructure.dependency.scopes import IScoped
from infrastructure.exceptions.OperationalException import OperationalException
from infrastructure.logging.SqlLogger import SqlLogger
from models.configs.ApplicationConfig import ApplicationConfig
from models.dao.aps.ApSchedulerJob import ApSchedulerJob
from models.dao.operation import DataOperation
from models.dao.operation.DataOperationJob import DataOperationJob


class JobOperationService(IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 data_operation_service: DataOperationService,
                 data_operation_job_service: DataOperationJobService,
                 application_config: ApplicationConfig,
                 scheduler_rpc_client_service: SchedulerRpcClientService,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.ap_scheduler_job_repository = repository_provider.get(ApSchedulerJob)
        self.scheduler_rpc_client_service = scheduler_rpc_client_service
        self.application_config = application_config
        self.data_operation_job_service = data_operation_job_service
        self.data_operation_service = data_operation_service
        self.sql_logger = sql_logger

    def get_ap_scheduler_with_retry(self, job_id, retry: int = 0) -> ApSchedulerJob:
        ap_scheduler_job = self.ap_scheduler_job_repository.first(JobId=job_id)
        if ap_scheduler_job is None and retry < 3:
            time.sleep(2)
            ap_scheduler_job = self.get_ap_scheduler_with_retry(job_id, retry + 1)
        return ap_scheduler_job

    def delete_job(self, data_operation_job_id: int, ap_scheduler_job_id):
        ap_scheduler_job = self.ap_scheduler_job_repository.first(IsDeleted=0,
                                                                  Id=ap_scheduler_job_id)
        if ap_scheduler_job is not None:
            try:
                job = self.scheduler_rpc_client_service.delete_job(ap_scheduler_table_job_id=ap_scheduler_job.JobId)

            except Exception as ex:
                pass

        self.data_operation_job_service.delete_by_id(id=data_operation_job_id)

    def delete_existing_cron_jobs(self, data_operation_id):
        data_operation_jobs: List[DataOperationJob] = self.data_operation_job_service.get_all_by_data_operation_id(
            data_operation_id=data_operation_id).all()
        for data_operation_job in data_operation_jobs:
            if data_operation_job.Cron is not None:
                self.delete_job(data_operation_job_id=data_operation_job.Id,
                                ap_scheduler_job_id=data_operation_job.ApSchedulerJobId)

    def update_job_with_cron(self, data_operation_id: int, cron: str, start_date: datetime = None,
                             end_date: datetime = None) -> ApSchedulerJob:
        self.delete_existing_cron_jobs(data_operation_id=data_operation_id)
        ap_scheduler_job = self.add_job_with_cron(
            cron=cron,
            start_date=start_date,
            end_date=end_date,
            args=(None, data_operation_id,))
        return ap_scheduler_job

    def check_cron_initialized_jobs(self, data_operation_id):
        data_operation_jobs: List[DataOperationJob] = self.data_operation_job_service.get_all_by_data_operation_id(
            data_operation_id=data_operation_id).all()
        for job in data_operation_jobs:
            if job.Cron is not None and job.IsDeleted == 0:
                return True
        return False

    def insert_job_with_cron(self, data_operation_id: DataOperation, cron: str, start_date: datetime = None,
                             end_date: datetime = None) -> ApSchedulerJob:
        check = self.check_cron_initialized_jobs(data_operation_id=data_operation_id)
        if check:
            raise OperationalException("Job already initialized with cron. ")
        ap_scheduler_job = self.add_job_with_cron(
            cron=cron, start_date=start_date, end_date=end_date,
            args=(None, data_operation_id,))

        return ap_scheduler_job

    def get_cron_job(self, data_operation_id: int):
        data_operation_jobs: List[DataOperationJob] = self.data_operation_job_service.get_all_by_data_operation_id(
            data_operation_id=data_operation_id).all()
        if data_operation_jobs is None or len(data_operation_jobs) == 0:
            return None
        found_cron_job: DataOperationJob = None
        for data_operation_job in data_operation_jobs:
            if data_operation_job.Cron is not None:
                found_cron_job = data_operation_job
                break
        if found_cron_job is None:
            return None
        else:
            return found_cron_job

    def create_job_with_cron(self, operation_name: str, cron: str, start_date: datetime = None,
                             end_date: datetime = None) -> DataOperationJob:

        if cron is None or cron == '':
            raise OperationalException("Cron required")
        data_operation = self.data_operation_service.get_by_name(name=operation_name)
        if data_operation is None:
            raise OperationalException("Data operation not found")

        if start_date is not None and start_date != '':
            job_start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        else:
            job_start_date = datetime.now().astimezone()
        if end_date is not None and end_date != '':
            job_end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        else:
            job_end_date = None
        cron_job = self.get_cron_job(data_operation_id=data_operation.Id)
        if cron_job is None:
            ap_scheduler_job = self.insert_job_with_cron(data_operation_id=data_operation.Id, cron=cron,
                                                         start_date=job_start_date,
                                                         end_date=job_end_date)
        else:
            ap_scheduler_job = self.update_job_with_cron(data_operation_id=data_operation.Id, cron=cron,
                                                         start_date=job_start_date,
                                                         end_date=job_end_date)

        data_operation_job = self.data_operation_job_service.insert_data_operation_job(
            ap_scheduler_job=ap_scheduler_job,
            data_operation=data_operation,
            cron=cron, start_date=start_date,
            end_date=end_date)
        self.repository_provider.commit()
        return data_operation_job

    def add_job_with_cron(self, cron, start_date=None, end_date=None, args=None,
                          kwargs=None) -> ApSchedulerJob:

        job = self.scheduler_rpc_client_service.add_job_with_cron(cron=cron, start_date=start_date, end_date=end_date, args=args,
                                                                  kwargs=kwargs)
        if job is None :
            raise OperationalException("Scheduler server getting error")
        ap_scheduler_job = self.get_ap_scheduler_with_retry(job.id)
        return ap_scheduler_job

    def add_job_with_date(self, run_date, args=None, kwargs=None) -> ApSchedulerJob:
        job = self.scheduler_rpc_client_service.add_job_with_date(run_date=run_date, args=args,
                                                                  kwargs=kwargs)
        if job is None :
            raise OperationalException("Scheduler server getting error")
        ap_scheduler_job = self.get_ap_scheduler_with_retry(job.id)
        return ap_scheduler_job

    #######################################################################################
    def insert_job_with_date(self, operation_name: str, run_date: datetime = None):
        data_operation = self.data_operation_service.get_by_name(name=operation_name)
        if data_operation is None:
            raise OperationalException("Data operation not found")
        start_date = datetime.now().astimezone()
        ap_scheduler_job = self.add_job_with_date(
            run_date=start_date, args=(None, data_operation.Id,))

        data_operation_job = self.data_operation_job_service.insert_data_operation_job(
            ap_scheduler_job=ap_scheduler_job,
            data_operation=data_operation,
            cron=None, start_date=start_date,
            end_date=None)
        self.repository_provider.commit()
        return data_operation_job

    def delete_scheduler_cron_job(self, data_operation_name):
        data_operation = self.data_operation_service.get_by_name(name=data_operation_name)
        if data_operation is None:
            raise OperationalException("Data operation not found")

        check = self.check_cron_initialized_jobs(data_operation_id=data_operation.Id)
        if not check:
            raise OperationalException("Cron Job not found.")

        self.delete_existing_cron_jobs(data_operation_id=data_operation.Id)
        self.repository_provider.commit()

    def delete_scheduler_date_job(self, data_operation_job_id):

        data_operation_job: DataOperationJob = self.data_operation_job_service.get_by_id(id=data_operation_job_id)
        if data_operation_job is None:
            raise OperationalException("Data operation job not found")

        self.delete_job(data_operation_job_id=data_operation_job.Id,
                        ap_scheduler_job_id=data_operation_job.ApSchedulerJobId)
        self.repository_provider.commit()
