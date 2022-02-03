from injector import inject
from pdip.cqrs import ICommandHandler, Dispatcher
from pdip.data.repository import RepositoryProvider
from pdip.integrator.domain.enums.events import EVENT_EXECUTION_INTEGRATION_EXECUTE_TARGET
from pdip.logging.loggers.sql import SqlLogger

from src.application.Events.ExecuteOperationIntegrationTarget.ExecuteOperationIntegrationTargetCommand import \
    ExecuteOperationIntegrationTargetCommand
from src.application.operation.services.DataOperationJobExecutionIntegrationService import \
    DataOperationJobExecutionIntegrationService


class ExecuteOperationIntegrationTargetCommandHandler(ICommandHandler[ExecuteOperationIntegrationTargetCommand]):
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

    def handle(self, command: ExecuteOperationIntegrationTargetCommand):
        try:
            message = f'{command.request.OperationIntegration.Id}-{command.request.OperationIntegration.Order}-{command.request.OperationIntegration.Name}-Target integration completed. (Affected Row Count:{command.request.RowCount})'
            self.logger.info(message, job_id=command.request.OperationIntegration.Execution.OperationExecutionId)
            self.data_operation_job_execution_integration_service.create_event(
                data_operation_job_execution_integration_id=command.request.OperationIntegration.Execution.Id,
                event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_TARGET, affected_row=command.request.RowCount)
        except Exception as ex:
            self.logger.exception(ex, str(ex))
            raise Exception(str(ex))
