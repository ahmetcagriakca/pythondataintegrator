from injector import inject
from pdip.cqrs import ICommandHandler, Dispatcher
from pdip.integrator.domain.enums.events import EVENT_EXECUTION_INTEGRATION_FINISHED
from pdip.logging.loggers.sql import SqlLogger

from process.application.Events.ExecuteOperationIntegrationFinish.ExecuteOperationIntegrationFinishCommand import \
    ExecuteOperationIntegrationFinishCommand
from process.application.operation.services.DataOperationJobExecutionIntegrationService import \
    DataOperationJobExecutionIntegrationService
from process.domain.enums.StatusTypes import StatusTypes


class ExecuteOperationIntegrationFinishCommandHandler(ICommandHandler[ExecuteOperationIntegrationFinishCommand]):
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

    def handle(self, command: ExecuteOperationIntegrationFinishCommand):
        try:
            if command.request.Exception is not None:
                message = f'{command.request.OperationIntegration.Id}-{command.request.OperationIntegration.Order}-{command.request.OperationIntegration.Name}-{command.request.Message}'
                self.logger.exception(command.request.Exception, message,
                                      job_id=command.request.OperationIntegration.Execution.OperationExecutionId)
                self.update_status(
                    data_operation_job_execution_integration_id=command.request.OperationIntegration.Execution.Id,
                    status=StatusTypes.Error,
                    event_code=EVENT_EXECUTION_INTEGRATION_FINISHED,
                    message=message
                )
            else:
                message = f'{command.request.OperationIntegration.Id}-{command.request.OperationIntegration.Order}-{command.request.OperationIntegration.Name}-{command.request.Message}'
                self.logger.info(message, job_id=command.request.OperationIntegration.Execution.OperationExecutionId)
                self.update_status(
                    data_operation_job_execution_integration_id=command.request.OperationIntegration.Execution.Id,
                    status=StatusTypes.Finish,
                    event_code=EVENT_EXECUTION_INTEGRATION_FINISHED,
                    message=message
                )
        except Exception as ex:
            self.logger.exception(ex, str(ex))
            raise Exception(str(ex))

    def update_status(self,
                      data_operation_job_execution_integration_id: int,
                      message: str,
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

        self.data_operation_job_execution_integration_service.update_log(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            log=message)
