from injector import inject
from pdip.cqrs import ICommandHandler, Dispatcher
from pdip.integrator.domain.enums import StatusTypes
from pdip.integrator.domain.enums.events import EVENT_EXECUTION_STARTED
from pdip.logging.loggers.sql import SqlLogger

from src.application.Events.ExecuteOperationStart.ExecuteOperationStartCommand import \
    ExecuteOperationStartCommand
from src.application.operation.services.DataOperationJobExecutionService import DataOperationJobExecutionService


class ExecuteOperationStartCommandHandler(ICommandHandler[ExecuteOperationStartCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 logger: SqlLogger,
                 data_operation_job_execution_service: DataOperationJobExecutionService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_operation_job_execution_service = data_operation_job_execution_service
        self.logger = logger
        self.dispatcher = dispatcher

    def handle(self, command: ExecuteOperationStartCommand):
        try:
            message = f'{command.request.Operation.Id}-{command.request.Operation.Name} started.'
            self.__event(
                data_operation_job_execution_id=command.request.Operation.Execution.Id,
                message=message,
                status=StatusTypes.Start,
                event_code=EVENT_EXECUTION_STARTED
            )
        except Exception as ex:
            self.logger.exception(ex, str(ex))
            raise Exception(str(ex))

    def __event(self, data_operation_job_execution_id, message: str, status: StatusTypes, event_code: int):
        self.logger.info(
            message,
            job_id=data_operation_job_execution_id
        )
        self.data_operation_job_execution_service.create_event(
            data_operation_execution_id=data_operation_job_execution_id,
            event_code=event_code
        )
        self.data_operation_job_execution_service.update_status(
            data_operation_job_execution_id=data_operation_job_execution_id,
            status_id=status.value
        )
