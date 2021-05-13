from datetime import datetime
from injector import inject

from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from models.dao.common import OperationEvent
from models.dao.common.Status import Status
from models.dao.operation import DataOperationJobExecution, DataOperationJobExecutionIntegration, \
    DataOperationJobExecutionIntegrationEvent, DataOperationIntegration
from models.enums.events import EVENT_EXECUTION_INTEGRATION_INITIALIZED


class DataOperationJobExecutionIntegrationService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 ):
        self.database_session_manager = database_session_manager
        self.data_operation_job_execution_repository: Repository[DataOperationJobExecution] = Repository[
            DataOperationJobExecution](database_session_manager)
        self.status_repository: Repository[Status] = Repository[Status](database_session_manager)
        self.operation_event_repository: Repository[OperationEvent] = Repository[
            OperationEvent](database_session_manager)

        self.data_operation_job_execution_integration_repository: Repository[DataOperationJobExecutionIntegration] = \
            Repository[
                DataOperationJobExecutionIntegration](database_session_manager)
        self.data_operation_job_execution_integration_event_repository: Repository[
            DataOperationJobExecutionIntegrationEvent] = Repository[
            DataOperationJobExecutionIntegrationEvent](database_session_manager)

    def create(self, data_operation_job_execution_id,
               data_operation_integration: DataOperationIntegration):
        data_operation_job_execution = self.data_operation_job_execution_repository.first(
            Id=data_operation_job_execution_id)

        status = self.status_repository.first(Id=1)
        data_operation_job_execution_integration = DataOperationJobExecutionIntegration(
            DataOperationJobExecution=data_operation_job_execution,
            DataOperationIntegration=data_operation_integration,
            Status=status,
            Limit=data_operation_integration.Limit,
            ProcessCount=data_operation_integration.ProcessCount)
        self.data_operation_job_execution_integration_repository.insert(data_operation_job_execution_integration)
        operation_event = self.operation_event_repository.first(Code=EVENT_EXECUTION_INTEGRATION_INITIALIZED)
        data_operation_job_execution_integration_event = DataOperationJobExecutionIntegrationEvent(
            EventDate=datetime.now(),
            DataOperationJobExecutionIntegration=data_operation_job_execution_integration,
            Event=operation_event)
        self.data_operation_job_execution_integration_event_repository.insert(
            data_operation_job_execution_integration_event)
        self.database_session_manager.commit()
        return data_operation_job_execution_integration

    def update_status(self,
                      data_operation_job_execution_integration_id: int = None,
                      status_id: int = None, is_finished: bool = False):
        data_operation_job_execution_integration = self.data_operation_job_execution_integration_repository.first(
            Id=data_operation_job_execution_integration_id)
        status = self.status_repository.first(Id=status_id)
        if is_finished:
            data_operation_job_execution_integration.EndDate = datetime.now()

        data_operation_job_execution_integration.Status = status
        self.database_session_manager.commit()
        return data_operation_job_execution_integration

    def update_source_data_count(self,
                                 data_operation_job_execution_integration_id: int = None,
                                 source_data_count=None):
        data_operation_job_execution_integration = self.data_operation_job_execution_integration_repository.first(
            Id=data_operation_job_execution_integration_id)

        data_operation_job_execution_integration.SourceDataCount = source_data_count
        self.database_session_manager.commit()
        return data_operation_job_execution_integration

    def update_log(self,
                   data_operation_job_execution_integration_id: int = None,
                   log=None):
        data_operation_job_execution_integration = self.data_operation_job_execution_integration_repository.first(
            Id=data_operation_job_execution_integration_id)

        data_operation_job_execution_integration.Log = log[0:1000]
        self.database_session_manager.commit()
        return data_operation_job_execution_integration

    def create_event(self, data_operation_execution_integration_id,
                     event_code,
                     affected_row=None) -> DataOperationJobExecutionIntegrationEvent:
        data_operation_job_execution_integration = self.data_operation_job_execution_integration_repository.first(
            Id=data_operation_execution_integration_id)
        operation_event = self.operation_event_repository.first(Code=event_code)
        data_operation_job_execution_integration_event = DataOperationJobExecutionIntegrationEvent(
            EventDate=datetime.now(),
            AffectedRowCount=affected_row,
            DataOperationJobExecutionIntegration=data_operation_job_execution_integration,
            Event=operation_event)
        self.data_operation_job_execution_integration_event_repository.insert(
            data_operation_job_execution_integration_event)
        self.database_session_manager.commit()
        return data_operation_job_execution_integration
