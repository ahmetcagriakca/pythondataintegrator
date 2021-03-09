import time
from datetime import datetime
from typing import List

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
from infrastructor.multi_processing.ParallelMultiProcessing import ParallelMultiProcessing, TaskData, ProcessBaseData
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

    def delete_job(self, data_operation_job_id: int, ap_scheduler_job_id):
        ap_scheduler_job = self.ap_scheduler_job_repository.first(IsDeleted=0,
                                                                  Id=ap_scheduler_job_id)
        if ap_scheduler_job is not None:
            try:
                self.job_scheduler.remove_job(job_id=ap_scheduler_job.JobId)
            except Exception as ex:
                pass
        self.data_operation_job_repository.delete_by_id(data_operation_job_id)

    def delete_existing_cron_jobs(self, data_operation_id):
        data_operation_jobs: List[DataOperationJob] = self.data_operation_job_repository.filter_by(IsDeleted=0,
                                                                                                   DataOperationId=data_operation_id).all()
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
        data_operation_jobs = self.data_operation_job_repository.filter_by(IsDeleted=0,
                                                                           DataOperationId=data_operation_id).all()
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
        data_operation_jobs = self.data_operation_job_repository.filter_by(IsDeleted=0,
                                                                           DataOperationId=data_operation_id).all()
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

        data_operation_job = self.insert_data_operation_job(ap_scheduler_job, data_operation, cron, start_date,
                                                            end_date)
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
        job = self.job_scheduler.add_job_with_date(job_function=job_function, run_date=run_date, args=args,
                                                   kwargs=kwargs)
        ap_scheduler_job = self.get_ap_scheduler_with_retry(job.id)
        return ap_scheduler_job

    def insert_data_operation_job(self, ap_scheduler_job, data_operation, cron, start_date, end_date):
        data_operation_job = DataOperationJob(StartDate=start_date, EndDate=end_date,
                                              Cron=cron, ApSchedulerJob=ap_scheduler_job,
                                              DataOperation=data_operation)
        self.data_operation_job_repository.insert(data_operation_job)
        return data_operation_job

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
        data_operation_job = self.insert_data_operation_job(ap_scheduler_job, data_operation, None, start_date, None)
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

        data_operation_job: DataOperationJob = self.data_operation_job_repository.first(IsDeleted=0,
                                                                                        Id=data_operation_job_id)
        if data_operation_job is None:
            raise OperationalException("Data operation job not found")

        self.delete_job(data_operation_job_id=data_operation_job.Id,
                        ap_scheduler_job_id=data_operation_job.ApSchedulerJobId)
        self.database_session_manager.commit()

    @staticmethod
    def job_start_data_operation(job_id, data_operation_id: int):
        start = time.time()
        start_datetime = datetime.now()

        sql_logger = SqlLogger()
        sql_logger.info(f"{job_id}-{data_operation_id} Data Operations Started")
        parallel_multi_processing = ParallelMultiProcessing(1)
        parallel_multi_processing.configure_process()
        parallel_multi_processing.start_processes(process_id=data_operation_id, job_id=job_id,
                                                  process_function=DataOperationJobService.job_start_thread)
        data = ProcessBaseData(Id=1)
        td = TaskData(data)
        parallel_multi_processing.add_task(td)
        parallel_multi_processing.check_processes()
        parallel_multi_processing.finish_all_processes()
        end_datetime = datetime.now()
        end = time.time()
        sql_logger.info(f"{job_id}-{data_operation_id} Start :{start_datetime}")
        sql_logger.info(f"{job_id}-{data_operation_id} End :{end_datetime}")
        sql_logger.info(f"{job_id}-{data_operation_id} ElapsedTime :{end - start}")

        unprocessed_task = parallel_multi_processing.unprocessed_tasks()
        if unprocessed_task[0].Data.State == 2:
            sql_logger.info(
                f"{job_id}-{data_operation_id} Data Operations Finished With Error: {unprocessed_task[0].Data.Message}")
            exc = Exception(unprocessed_task[0].Data.Traceback + '\n' + str(unprocessed_task[0].Data.Exception))
            raise exc
        sql_logger.info(f"{job_id}-{data_operation_id} Data Operations Finished")
        del parallel_multi_processing
        return unprocessed_task[0].Data.Result
