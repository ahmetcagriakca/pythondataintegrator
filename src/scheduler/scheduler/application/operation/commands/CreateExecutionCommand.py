from datetime import datetime
from injector import inject
from pdip.configuration.models.database import DatabaseConfig
from pdip.data import RepositoryProvider
from pdip.dependency.container import DependencyContainer
from pdip.exceptions import OperationalException
from pdip.logging.loggers.database import SqlLogger

from scheduler.domain.dao.common.Status import Status
from scheduler.domain.dao.common.OperationEvent import OperationEvent
from scheduler.domain.dao.operation.DataOperationJob import DataOperationJob
from scheduler.domain.dao.operation.DataOperationJobExecution import DataOperationJobExecution
from scheduler.domain.dao.operation.DataOperationJobExecutionEvent import DataOperationJobExecutionEvent
from scheduler.domain.dao.operation.DataOperation import DataOperation


class CreateExecutionCommand:
    @inject
    def __init__(self,
                 ):
        self.database_config = DependencyContainer.Instance.get(DatabaseConfig)
        self.repository_provider = RepositoryProvider(database_config=self.database_config,
                                                      database_session_manager=None)
        self.sql_logger = DependencyContainer.Instance.get(SqlLogger)

    def get_data_operation_by_id(self, id: int) -> DataOperationJob:
        entity = self.repository_provider.get(DataOperation).first(IsDeleted=0, Id=id)
        return entity

    def get_data_operation_job_by_operation_and_job_id(self, data_operation_id: int, job_id: int) -> DataOperationJob:
        entity = self.repository_provider.get(DataOperationJob).first(IsDeleted=0,
                                                                      DataOperationId=data_operation_id,
                                                                      ApSchedulerJobId=job_id)
        return entity

    def check(self, data_operation_id: int, job_id: int):
        data_operation = self.get_data_operation_by_id(id=data_operation_id)
        if data_operation is None:
            error = f'{data_operation_id}-{job_id} Data operation not found'
            self.sql_logger.error(error)
            return OperationalException(error)

        data_operation_job = self.get_data_operation_job_by_operation_and_job_id(
            data_operation_id=data_operation_id,
            job_id=job_id)
        if data_operation_job is None:
            error = f'{data_operation_id}-{job_id} Data operation job not found'
            self.sql_logger.error(error)
            return OperationalException(error)

    def execute(self, data_operation_id: int, job_id: int):
        self.check(data_operation_id, job_id)
        data_operation_job = self.get_data_operation_job_by_operation_and_job_id(
            data_operation_id=data_operation_id,
            job_id=job_id)
        status = self.repository_provider.get(Status).first(Id=1)
        data_operation_job_execution = DataOperationJobExecution(
            DataOperationJob=data_operation_job,
            Status=status,
            Definition=data_operation_job.DataOperation.Definition)
        self.repository_provider.get(DataOperationJobExecution).insert(data_operation_job_execution)
        operation_event = self.repository_provider.get(OperationEvent).first(Code=1)
        data_operation_job_execution_event = DataOperationJobExecutionEvent(
            EventDate=datetime.now(),
            DataOperationJobExecution=data_operation_job_execution,
            Event=operation_event)
        self.repository_provider.get(DataOperationJobExecutionEvent).insert(data_operation_job_execution_event)
        result = data_operation_job_execution.Id
        self.repository_provider.get(DataOperationJobExecutionEvent).commit()
        return result
