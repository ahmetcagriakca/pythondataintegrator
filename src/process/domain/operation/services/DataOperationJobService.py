from datetime import datetime

from injector import inject

from domain.operation.services.DataOperationJobExecutionService import DataOperationJobExecutionService
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.dependency.scopes import IScoped
from models.dao.aps import ApSchedulerJob
from models.dao.operation import DataOperationJob, DataOperation


class DataOperationJobService(IScoped):
    @inject
    def __init__(self,
                 data_operation_job_execution_service: DataOperationJobExecutionService,
                 repository_provider: RepositoryProvider,
                 ):
        super().__init__()
        self.repository_provider = repository_provider
        self.data_operation_job_repository = repository_provider.get(DataOperationJob)
        self.data_operation_job_execution_service = data_operation_job_execution_service

    def get_by_id(self, id: int) -> DataOperationJob:
        entity = self.data_operation_job_repository.first(IsDeleted=0, Id=id)
        return entity

    def get_all_by_data_operation_id(self, data_operation_id: int) -> DataOperationJob:
        entities = self.data_operation_job_repository.filter_by(IsDeleted=0,
                                                                DataOperationId=data_operation_id)
        return entities

    def get_by_job_id(self, job_id: int) -> DataOperationJob:
        entity = self.data_operation_job_repository.first(IsDeleted=0,
                                                          ApSchedulerJobId=job_id)
        return entity

    def get_by_operation_and_job_id(self, data_operation_id: int, job_id: int) -> DataOperationJob:
        entity = self.data_operation_job_repository.first(IsDeleted=0,
                                                          DataOperationId=data_operation_id,
                                                          ApSchedulerJobId=job_id)
        return entity

    def insert_data_operation_job(self, ap_scheduler_job: ApSchedulerJob, data_operation: DataOperation, cron,
                                  start_date, end_date):
        data_operation_job = DataOperationJob(StartDate=start_date, EndDate=end_date,
                                              Cron=cron, ApSchedulerJob=ap_scheduler_job,
                                              DataOperation=data_operation)
        self.data_operation_job_repository.insert(data_operation_job)
        return data_operation_job

    def remove_data_operation_job(self, ap_scheduler_job_id: int):
        data_operation_job = self.get_by_job_id(job_id=ap_scheduler_job_id)
        if data_operation_job is not None:
            self.delete_by_id(data_operation_job.Id)

    def delete_by_id(self, id):
        self.data_operation_job_repository.delete_by_id(id)

    def send_data_operation_miss_mail(self, ap_scheduler_job: ApSchedulerJob):
        data_operation_job = self.get_by_job_id(job_id=ap_scheduler_job.Id)
        if data_operation_job is not None:
            self.data_operation_job_execution_service.send_data_operation_miss_mail(
                data_operation_job=data_operation_job, next_run_time=ap_scheduler_job.NextRunTime)

    def check_removed_job(self, ap_scheduler_job_id):
        EVENT_JOB_REMOVED = 2 ** 10
        job_detail_query = self.database_session_manager.session.query(
            ApSchedulerJob, ApSchedulerEvent, ApSchedulerJobEvent
        ) \
            .filter(ApSchedulerJobEvent.ApSchedulerJobId == ApSchedulerJob.Id) \
            .filter(ApSchedulerJobEvent.EventId == ApSchedulerEvent.Id) \
            .filter(ApSchedulerEvent.Code == EVENT_JOB_REMOVED) \
            .filter(ApSchedulerJob.Id == ap_scheduler_job_id)
        job_detail = job_detail_query.first()
        if job_detail is not None:
            self.remove_data_operation_job(ap_scheduler_job_id=job_detail.ApSchedulerJob.Id)
