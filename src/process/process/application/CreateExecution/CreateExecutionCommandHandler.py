from datetime import datetime

from injector import inject
from pdip.cqrs import ICommandHandler
from pdip.data.decorators import transactionhandler
from pdip.data.repository import RepositoryProvider
from pdip.exceptions import OperationalException
from pdip.logging.loggers.sql import SqlLogger

from process.application.CreateExecution.CreateExecutionCommand import CreateExecutionCommand
from process.domain.common.OperationEvent import OperationEvent
from process.domain.common.Status import Status
from process.domain.operation.DataOperation import DataOperation
from process.domain.operation.DataOperationJob import DataOperationJob
from process.domain.operation.DataOperationJobExecution import DataOperationJobExecution
from process.domain.operation.DataOperationJobExecutionEvent import DataOperationJobExecutionEvent


class CreateExecutionCommandHandler(ICommandHandler[CreateExecutionCommand]):
    @inject
    def __init__(self,
                 logger: SqlLogger,
                 repository_provider: RepositoryProvider,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger
        self.repository_provider = repository_provider

    @transactionhandler
    def handle(self, command: CreateExecutionCommand):
        self.check(
            data_operation_id=command.DataOperationId,
            job_id=command.JobId)
        data_operation_job = self.get_data_operation_job_by_operation_and_job_id(
            data_operation_id=command.DataOperationId,
            job_id=command.JobId)
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
        self.repository_provider.commit()
        self.repository_provider.close()
        return result

    def get_data_operation_by_id(self, id: int) -> DataOperationJob:
        entity = self.repository_provider.get(DataOperation).first(IsDeleted=0, Id=id)
        return entity

    def get_data_operation_job_by_operation_and_job_id(self, data_operation_id: int,
                                                       job_id: int) -> DataOperationJob:
        entity = self.repository_provider.get(DataOperationJob).first(IsDeleted=0,
                                                                      DataOperationId=data_operation_id,
                                                                      ApSchedulerJobId=job_id)
        return entity

    def check(self, data_operation_id: int, job_id: int):
        data_operation = self.get_data_operation_by_id(id=data_operation_id)
        if data_operation is None:
            error = f'{data_operation_id}-{job_id} Data operation not found'
            self.logger.error(error)
            return OperationalException(error)

        data_operation_job = self.get_data_operation_job_by_operation_and_job_id(
            data_operation_id=data_operation_id,
            job_id=job_id)
        if data_operation_job is None:
            error = f'{data_operation_id}-{job_id} Data operation job not found'
            self.logger.error(error)
            return OperationalException(error)
