from datetime import datetime
from injector import inject
from pdip.configuration.models.database import DatabaseConfig
from pdip.cqrs import ICommandHandler
from pdip.data import RepositoryProvider
from pdip.exceptions import OperationalException
from pdip.logging.loggers.database import SqlLogger

from scheduler.application.CreateExecution.CreateExecutionCommand import CreateExecutionCommand
from scheduler.domain.common.Status import Status
from scheduler.domain.common.OperationEvent import OperationEvent
from scheduler.domain.operation.DataOperationJob import DataOperationJob
from scheduler.domain.operation.DataOperationJobExecution import DataOperationJobExecution
from scheduler.domain.operation.DataOperationJobExecutionEvent import DataOperationJobExecutionEvent
from scheduler.domain.operation.DataOperation import DataOperation


class CreateExecutionCommandHandler(ICommandHandler[CreateExecutionCommand]):
    @inject
    def __init__(self,
                 database_config: DatabaseConfig,
                 sql_logger: SqlLogger,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database_config = database_config
        self.sql_logger = sql_logger

    def get_data_operation_by_id(self, repository_provider, id: int) -> DataOperationJob:
        entity = repository_provider.get(DataOperation).first(IsDeleted=0, Id=id)
        return entity

    def get_data_operation_job_by_operation_and_job_id(self, repository_provider, data_operation_id: int,
                                                       job_id: int) -> DataOperationJob:
        entity = repository_provider.get(DataOperationJob).first(IsDeleted=0,
                                                                 DataOperationId=data_operation_id,
                                                                 ApSchedulerJobId=job_id)
        return entity

    def check(self, repository_provider, data_operation_id: int, job_id: int):
        data_operation = self.get_data_operation_by_id(repository_provider=repository_provider, id=data_operation_id)
        if data_operation is None:
            error = f'{data_operation_id}-{job_id} Data operation not found'
            self.sql_logger.error(error)
            return OperationalException(error)

        data_operation_job = self.get_data_operation_job_by_operation_and_job_id(
            repository_provider=repository_provider,
            data_operation_id=data_operation_id,
            job_id=job_id)
        if data_operation_job is None:
            error = f'{data_operation_id}-{job_id} Data operation job not found'
            self.sql_logger.error(error)
            return OperationalException(error)

    def handle(self, command: CreateExecutionCommand):
        data_operation_id = command.DataOperationId
        job_id = command.JobId
        repository_provider = RepositoryProvider(database_config=self.database_config, database_session_manager=None)
        self.check(
            repository_provider=repository_provider,
            data_operation_id=data_operation_id,
            job_id=job_id)
        data_operation_job = self.get_data_operation_job_by_operation_and_job_id(
            repository_provider=repository_provider,
            data_operation_id=data_operation_id,
            job_id=job_id)
        status = repository_provider.get(Status).first(Id=1)
        data_operation_job_execution = DataOperationJobExecution(
            DataOperationJob=data_operation_job,
            Status=status,
            Definition=data_operation_job.DataOperation.Definition)
        repository_provider.get(DataOperationJobExecution).insert(data_operation_job_execution)
        operation_event = repository_provider.get(OperationEvent).first(Code=1)
        data_operation_job_execution_event = DataOperationJobExecutionEvent(
            EventDate=datetime.now(),
            DataOperationJobExecution=data_operation_job_execution,
            Event=operation_event)
        repository_provider.get(DataOperationJobExecutionEvent).insert(data_operation_job_execution_event)
        result = data_operation_job_execution.Id
        repository_provider.get(DataOperationJobExecutionEvent).commit()
        repository_provider.close()
        del repository_provider
        return result
