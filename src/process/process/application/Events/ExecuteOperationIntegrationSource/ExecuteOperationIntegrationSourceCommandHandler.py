from injector import inject
from pdip.cqrs import ICommandHandler, Dispatcher
from pdip.data.repository import RepositoryProvider
from pdip.integrator.domain.enums.events import EVENT_EXECUTION_INTEGRATION_EXECUTE_SOURCE
from pdip.logging.loggers.sql import SqlLogger

from process.application.Events.ExecuteOperationIntegrationSource.ExecuteOperationIntegrationSourceCommand import \
    ExecuteOperationIntegrationSourceCommand
from process.application.operation.services.DataOperationJobExecutionIntegrationService import \
    DataOperationJobExecutionIntegrationService


class ExecuteOperationIntegrationSourceCommandHandler(ICommandHandler[ExecuteOperationIntegrationSourceCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 logger: SqlLogger,
                 data_operation_job_execution_integration_service: DataOperationJobExecutionIntegrationService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger
        self.data_operation_job_execution_integration_service = data_operation_job_execution_integration_service
        self.dispatcher = dispatcher

    def handle(self, command: ExecuteOperationIntegrationSourceCommand):
        try:
            message = f'{command.request.OperationIntegration.Id}-{command.request.OperationIntegration.Order}-{command.request.OperationIntegration.Name}-Source integration completed. (Source Data Count:{command.request.RowCount}'
            self.logger.info(message, job_id=command.request.OperationIntegration.Execution.OperationExecutionId)
            self.data_operation_job_execution_integration_service.update_source_data_count(
                data_operation_job_execution_integration_id=command.request.OperationIntegration.Execution.Id,
                source_data_count=command.request.RowCount)
            self.data_operation_job_execution_integration_service.create_event(
                data_operation_job_execution_integration_id=command.request.OperationIntegration.Execution.Id,
                event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_SOURCE, affected_row=command.request.RowCount)
        except Exception as ex:
            self.logger.exception(ex, str(ex))
            raise Exception(str(ex))
