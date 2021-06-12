import time
from datetime import datetime
from typing import List

import rpyc
from apscheduler.triggers.cron import CronTrigger
from injector import inject

from infrastructor.multi_processing.ProcessManager import ProcessManager
from domain.operation.execution.services.OperationExecution import OperationExecution
from domain.operation.services.DataOperationJobService import DataOperationJobService
from domain.operation.services.DataOperationService import DataOperationService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exceptions.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.scheduler.JobScheduler import JobScheduler
from models.configs.ApplicationConfig import ApplicationConfig
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
                 job_scheduler: JobScheduler,
                 data_operation_job_service: DataOperationJobService,
                 application_config: ApplicationConfig
                 ):
        self.application_config = application_config
        self.data_operation_job_service = data_operation_job_service
        self.data_operation_service = data_operation_service
        self.job_scheduler = job_scheduler
        self.database_session_manager = database_session_manager
        self.ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
            database_session_manager)

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
                self.job_scheduler.remove_job(job_id=ap_scheduler_job.JobId)
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
        ap_scheduler_job = self.add_job_with_cron(job_function=JobOperationService.job_start_data_operation,
                                                  cron=cron, start_date=start_date, end_date=end_date,
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
        ap_scheduler_job = self.add_job_with_cron(job_function=JobOperationService.job_start_data_operation,
                                                  cron=cron, start_date=start_date, end_date=end_date,
                                                  args=(None, data_operation_id,))

        return ap_scheduler_job

    def get_cron_job(self, data_operation_id: int):
        data_operation_jobs: List[DataOperationJob] = self.data_operation_job_service.get_all_by_data_operation_id(
            data_operation_id=data_operation_id).all()
        if data_operation_jobs is None or len(data_operation_jobs) == 0:
            return None
        founded_cron_job: DataOperationJob = None
        for data_operation_job in data_operation_jobs:
            if data_operation_job.Cron is not None:
                founded_cron_job = data_operation_job
                break
        if founded_cron_job is None:
            return None
        else:
            return founded_cron_job

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
        self.database_session_manager.commit()
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
        if not self.application_config.process_node:
            conn = rpyc.connect('localhost', 7300)
            job = conn.root.add_job_with_date('server:domain.job.services.JobOperationService.job_start_data_operation', run_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), args=args)
        else:
            job = self.job_scheduler.add_job_with_date(job_function=job_function, run_date=run_date, args=args,
                                                       kwargs=kwargs)
        ap_scheduler_job = self.get_ap_scheduler_with_retry(job.id)
        return ap_scheduler_job

    #######################################################################################
    def insert_job_with_date(self, operation_name: str, run_date: datetime = None):
        data_operation = self.data_operation_service.get_by_name(name=operation_name)
        if data_operation is None:
            raise OperationalException("Data operation not found")
        if run_date is not None and run_date != '':
            start_date = datetime.strptime(run_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        else:
            start_date = datetime.now().astimezone()
        ap_scheduler_job = self.add_job_with_date(job_function=JobOperationService.job_start_data_operation,
                                                  run_date=start_date, args=(None, data_operation.Id,))

        data_operation_job = self.data_operation_job_service.insert_data_operation_job(
            ap_scheduler_job=ap_scheduler_job,
            data_operation=data_operation,
            cron=None, start_date=start_date,
            end_date=None)
        self.database_session_manager.commit()
        return data_operation_job

    def delete_scheduler_cron_job(self, data_operation_name):
        data_operation = self.data_operation_service.get_by_name(name=data_operation_name)
        if data_operation is None:
            raise OperationalException("Data operation not found")

        check = self.check_cron_initialized_jobs(data_operation_id=data_operation.Id)
        if not check:
            raise OperationalException("Cron Job not founded.")

        self.delete_existing_cron_jobs(data_operation_id=data_operation.Id)
        self.database_session_manager.commit()

    def delete_scheduler_date_job(self, data_operation_job_id):

        data_operation_job: DataOperationJob = self.data_operation_job_service.get_by_id(id=data_operation_job_id)
        if data_operation_job is None:
            raise OperationalException("Data operation job not found")

        self.delete_job(data_operation_job_id=data_operation_job.Id,
                        ap_scheduler_job_id=data_operation_job.ApSchedulerJobId)
        self.database_session_manager.commit()

    @staticmethod
    def job_start_data_operation(job_id, data_operation_id: int):
        """
        :param job_id: Ap Scheduler Job Id
        :param data_operation_id: Data Operation Id
        :return:
        TODO: Move this method to OperationExecution, but needs update as it will affect existing cron jobs
        """
        start = time.time()
        start_datetime = datetime.now()

        sql_logger = SqlLogger()
        sql_logger.info(f"{job_id}-{data_operation_id} Data Operations Started")
        operation_process_manager = ProcessManager()

        operation_kwargs = {
            "data_operation_id": data_operation_id,
            "job_id": job_id,
        }

        operation_process_manager.start_processes(process_count=1,
                                                  target_method=OperationExecution.start_operation,
                                                  kwargs=operation_kwargs)
        process_results = operation_process_manager.get_results()
        end_datetime = datetime.now()
        end = time.time()
        sql_logger.info(f"{job_id}-{data_operation_id} Start :{start_datetime}")
        sql_logger.info(f"{job_id}-{data_operation_id} End :{end_datetime}")
        sql_logger.info(f"{job_id}-{data_operation_id} ElapsedTime :{end - start}")
        if process_results[0].State == 4:
            sql_logger.info(
                f"{job_id}-{data_operation_id} Data Operations Finished With Error: {process_results[0].Exception}")
            exc = Exception(process_results[0].Traceback + '\n' + str(process_results[0].Exception))
            del operation_process_manager
            del sql_logger
            raise exc
        else:
            sql_logger.info(f"{job_id}-{data_operation_id} Data Operations Finished")
            del operation_process_manager
            del sql_logger
            return process_results[0].Result
