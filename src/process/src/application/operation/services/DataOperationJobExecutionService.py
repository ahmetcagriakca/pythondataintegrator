from datetime import datetime

from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from src.domain.common import OperationEvent
from src.domain.common.Status import Status
from src.domain.operation import DataOperationJobExecution
from src.domain.operation.DataOperationJobExecutionEvent import DataOperationJobExecutionEvent


class DataOperationJobExecutionService(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.data_operation_job_execution_repository = repository_provider.get(DataOperationJobExecution)
        self.status_repository = repository_provider.get(Status)
        self.operation_event_repository = repository_provider.get(OperationEvent)
        self.data_operation_job_execution_event_repository = repository_provider.get(DataOperationJobExecutionEvent)

    def update_status(self, data_operation_job_execution_id: int = None,
                      status_id: int = None, is_finished: bool = False):
        data_operation_job_execution = self.data_operation_job_execution_repository.first(
            Id=data_operation_job_execution_id)
        status = self.status_repository.first(Id=status_id)
        if is_finished:
            data_operation_job_execution.EndDate = datetime.now()

        data_operation_job_execution.Status = status
        self.repository_provider.commit()
        return data_operation_job_execution

    def create_event(self, data_operation_execution_id,
                     event_code) -> DataOperationJobExecutionEvent:
        data_operation_job_execution = self.data_operation_job_execution_repository.first(
            Id=data_operation_execution_id)
        operation_event = self.operation_event_repository.first(Code=event_code)
        data_operation_job_execution_event = DataOperationJobExecutionEvent(
            EventDate=datetime.now(),
            DataOperationJobExecution=data_operation_job_execution,
            Event=operation_event)
        self.data_operation_job_execution_event_repository.insert(data_operation_job_execution_event)
        self.repository_provider.commit()
        return data_operation_job_execution_event
