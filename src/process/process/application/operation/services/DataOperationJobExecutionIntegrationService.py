from datetime import datetime

from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from process.domain.common import OperationEvent
from process.domain.common.Status import Status
from process.domain.enums.events import EVENT_EXECUTION_INTEGRATION_INITIALIZED
from process.domain.operation import DataOperationJobExecution, DataOperationJobExecutionIntegration, \
    DataOperationJobExecutionIntegrationEvent, DataOperationIntegration


class DataOperationJobExecutionIntegrationService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.data_operation_job_execution_repository = repository_provider.get(DataOperationJobExecution)
        self.status_repository = repository_provider.get(Status)
        self.operation_event_repository = repository_provider.get(OperationEvent)
        self.data_operation_integration_repository = repository_provider.get(
            DataOperationIntegration)
        self.data_operation_job_execution_integration_repository = repository_provider.get(
            DataOperationJobExecutionIntegration)
        self.data_operation_job_execution_integration_event_repository = repository_provider.get(
            DataOperationJobExecutionIntegrationEvent)

    def create(self, data_operation_job_execution_id,
               data_operation_integration_id: int, limit: int, process_count: int):
        data_operation_job_execution = self.data_operation_job_execution_repository.first(
            Id=data_operation_job_execution_id)

        status = self.status_repository.first(Id=1)
        data_operation_integration = self.data_operation_integration_repository.get_by_id(data_operation_integration_id)
        data_operation_job_execution_integration = DataOperationJobExecutionIntegration(
            DataOperationJobExecution=data_operation_job_execution,
            DataOperationIntegration=data_operation_integration,
            Status=status,
            Limit=limit,
            ProcessCount=process_count)
        self.data_operation_job_execution_integration_repository.insert(data_operation_job_execution_integration)
        operation_event = self.operation_event_repository.first(Code=EVENT_EXECUTION_INTEGRATION_INITIALIZED)
        data_operation_job_execution_integration_event = DataOperationJobExecutionIntegrationEvent(
            EventDate=datetime.now(),
            DataOperationJobExecutionIntegration=data_operation_job_execution_integration,
            Event=operation_event)
        self.data_operation_job_execution_integration_event_repository.insert(
            data_operation_job_execution_integration_event)
        data_operation_job_execution_integration_id = data_operation_job_execution_integration.Id
        self.repository_provider.commit()
        return data_operation_job_execution_integration_id

    def update_status(self,
                      data_operation_job_execution_integration_id: int = None,
                      status_id: int = None, is_finished: bool = False):
        data_operation_job_execution_integration = self.data_operation_job_execution_integration_repository.first(
            Id=data_operation_job_execution_integration_id)
        status = self.status_repository.first(Id=status_id)
        if is_finished:
            data_operation_job_execution_integration.EndDate = datetime.now()

        data_operation_job_execution_integration.Status = status
        self.repository_provider.commit()
        return data_operation_job_execution_integration

    def update_source_data_count(self,
                                 data_operation_job_execution_integration_id: int = None,
                                 source_data_count=None):
        data_operation_job_execution_integration = self.data_operation_job_execution_integration_repository.first(
            Id=data_operation_job_execution_integration_id)

        data_operation_job_execution_integration.SourceDataCount = source_data_count
        self.repository_provider.commit()
        return data_operation_job_execution_integration

    def update_log(self,
                   data_operation_job_execution_integration_id: int = None,
                   log=None):
        data_operation_job_execution_integration = self.data_operation_job_execution_integration_repository.first(
            Id=data_operation_job_execution_integration_id)

        data_operation_job_execution_integration.Log = log[0:1000]
        self.repository_provider.commit()
        return data_operation_job_execution_integration

    def create_event(self, data_operation_job_execution_integration_id,
                     event_code,
                     affected_row=None) -> DataOperationJobExecutionIntegrationEvent:
        data_operation_job_execution_integration = self.data_operation_job_execution_integration_repository.first(
            Id=data_operation_job_execution_integration_id)
        operation_event = self.operation_event_repository.first(Code=event_code)
        data_operation_job_execution_integration_event = DataOperationJobExecutionIntegrationEvent(
            EventDate=datetime.now(),
            AffectedRowCount=affected_row,
            DataOperationJobExecutionIntegration=data_operation_job_execution_integration,
            Event=operation_event)
        self.data_operation_job_execution_integration_event_repository.insert(
            data_operation_job_execution_integration_event)
        self.repository_provider.commit()
        return data_operation_job_execution_integration
