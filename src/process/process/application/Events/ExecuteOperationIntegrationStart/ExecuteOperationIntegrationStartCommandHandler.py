from injector import inject
from pdip.cqrs import ICommandHandler, Dispatcher
from pdip.integrator.domain.enums import StatusTypes
from pdip.integrator.domain.enums.events import EVENT_EXECUTION_INTEGRATION_STARTED
from pdip.logging.loggers.sql import SqlLogger

from process.application.Events.ExecuteOperationIntegrationStart.ExecuteOperationIntegrationStartCommand import \
    ExecuteOperationIntegrationStartCommand
from process.application.operation.services.DataOperationJobExecutionIntegrationService import \
    DataOperationJobExecutionIntegrationService


class ExecuteOperationIntegrationStartCommandHandler(ICommandHandler[ExecuteOperationIntegrationStartCommand]):
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

    def handle(self, command: ExecuteOperationIntegrationStartCommand):
        try:
            message = f'{command.request.OperationIntegration.Id}-{command.request.OperationIntegration.Order}-{command.request.OperationIntegration.Name}-{command.request.Message}'
            self.logger.info(message, job_id=command.request.OperationIntegration.Execution.OperationExecutionId)
            self.update_status(
                data_operation_job_execution_integration_id=command.request.OperationIntegration.Execution.Id,
                status=StatusTypes.Start,
                event_code=EVENT_EXECUTION_INTEGRATION_STARTED
            )
        except Exception as ex:
            self.logger.exception(ex, str(ex))
            raise Exception(str(ex))

    def update_status(self,
                      data_operation_job_execution_integration_id: int,
                      status: StatusTypes,
                      event_code: int
                      ):
        self.data_operation_job_execution_integration_service.create_event(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            event_code=event_code
        )
        self.data_operation_job_execution_integration_service.update_status(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            status_id=status.value
        )
