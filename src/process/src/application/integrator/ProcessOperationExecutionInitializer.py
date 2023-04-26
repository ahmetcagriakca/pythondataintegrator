from datetime import datetime

from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.exceptions import OperationalException
from pdip.integrator.domain.enums import StatusTypes
from pdip.integrator.domain.enums.events import EVENT_EXECUTION_INITIALIZED
from pdip.integrator.initializer.execution.operation import OperationExecutionInitializer
from pdip.integrator.operation.domain import OperationBase
from pdip.logging.loggers.console import ConsoleLogger

from src.domain.common import Status, OperationEvent
from src.domain.operation import DataOperationJobExecution, DataOperationJobExecutionEvent, DataOperationJob


class ProcessOperationExecutionInitializer(OperationExecutionInitializer):
    @inject
    def __init__(self,
                 logger: ConsoleLogger,
                 repository_provider: RepositoryProvider
                 ):
        self.repository_provider = repository_provider
        self.logger = logger

    def initialize(self, operation: OperationBase):
        if operation.Execution is None or (
                operation.Execution.Id is None and operation.Execution.ApSchedulerJobId is None):
            raise Exception("ExecutionId or JobId required")
        if operation.Execution is not None and operation.Execution.Id is None:
            operation.Execution.Id = self.create_execution(operation_id=operation.Id,
                                                           ap_scheduler_job_id=operation.Execution.ApSchedulerJobId)
            for operation_integration in operation.Integrations:
                if operation_integration.Execution is not None:
                    operation_integration.Execution.OperationExecutionId = operation.Execution.Id
        return operation

    def create_execution(self, operation_id, ap_scheduler_job_id):
        data_operation_job = self.get_data_operation_job_by_operation_and_job_id(
            data_operation_id=operation_id,
            ap_scheduler_job_id=ap_scheduler_job_id)
        if data_operation_job is None:
            error = f'{operation_id}-{ap_scheduler_job_id} Data operation job not found'
            self.logger.error(error)
            raise OperationalException(error)

        status = self.repository_provider.get(Status).first(Id=StatusTypes.Initialized.value)
        data_operation_job_execution = DataOperationJobExecution(
            DataOperationJob=data_operation_job,
            Status=status,
            Definition=data_operation_job.DataOperation.Definition)
        self.repository_provider.get(DataOperationJobExecution).insert(data_operation_job_execution)
        operation_event = self.repository_provider.get(OperationEvent).first(Code=EVENT_EXECUTION_INITIALIZED)
        data_operation_job_execution_event = DataOperationJobExecutionEvent(
            EventDate=datetime.now(),
            DataOperationJobExecution=data_operation_job_execution,
            Event=operation_event)
        self.repository_provider.get(DataOperationJobExecutionEvent).insert(data_operation_job_execution_event)
        result = data_operation_job_execution.Id
        self.repository_provider.commit()
        self.repository_provider.close()
        return result

    def get_data_operation_job_by_operation_and_job_id(self, data_operation_id: int,
                                                       ap_scheduler_job_id: int) -> DataOperationJob:
        entity = self.repository_provider.get(DataOperationJob).first(IsDeleted=0,
                                                                      DataOperationId=data_operation_id,
                                                                      ApSchedulerJobId=ap_scheduler_job_id)
        return entity
