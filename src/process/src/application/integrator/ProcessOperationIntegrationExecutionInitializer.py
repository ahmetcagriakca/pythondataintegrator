from datetime import datetime

from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.integrator.domain.enums import StatusTypes
from pdip.integrator.domain.enums.events import EVENT_EXECUTION_INTEGRATION_INITIALIZED
from pdip.integrator.initializer.execution.integration import OperationIntegrationExecutionInitializer
from pdip.integrator.operation.domain import OperationIntegrationBase
from pdip.logging.loggers.console import ConsoleLogger

from src.domain.common import Status, OperationEvent
from src.domain.operation import DataOperationJobExecutionIntegration, DataOperationJobExecutionIntegrationEvent, \
    DataOperationJobExecution, DataOperationIntegration


class ProcessOperationIntegrationExecutionInitializer(OperationIntegrationExecutionInitializer):
    @inject
    def __init__(self, logger: ConsoleLogger,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.logger = logger

    def initialize(self, operation_integration: OperationIntegrationBase):
        data_operation_job_execution = self.repository_provider.get(DataOperationJobExecution).first(
            Id=operation_integration.Execution.OperationExecutionId)

        status = self.repository_provider.get(Status).first(Id=StatusTypes.Initialized.value)
        data_operation_integration = self.repository_provider.get(DataOperationIntegration).get_by_id(
            operation_integration.Id)
        data_operation_job_execution_integration = DataOperationJobExecutionIntegration(
            DataOperationJobExecution=data_operation_job_execution,
            DataOperationIntegration=data_operation_integration,
            Status=status,
            Limit=operation_integration.Limit,
            ProcessCount=operation_integration.ProcessCount)
        self.repository_provider.get(DataOperationJobExecutionIntegration).insert(
            data_operation_job_execution_integration)
        operation_event = self.repository_provider.get(OperationEvent).first(
            Code=EVENT_EXECUTION_INTEGRATION_INITIALIZED)
        data_operation_job_execution_integration_event = DataOperationJobExecutionIntegrationEvent(
            EventDate=datetime.now(),
            DataOperationJobExecutionIntegration=data_operation_job_execution_integration,
            Event=operation_event)
        self.repository_provider.get(DataOperationJobExecutionIntegrationEvent).insert(
            data_operation_job_execution_integration_event)
        data_operation_job_execution_integration_id = data_operation_job_execution_integration.Id
        self.repository_provider.commit()
        self.repository_provider.close()
        operation_integration.Execution.Id = data_operation_job_execution_integration_id
        return operation_integration
