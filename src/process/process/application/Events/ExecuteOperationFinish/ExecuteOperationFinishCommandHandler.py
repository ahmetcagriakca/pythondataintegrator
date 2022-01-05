from injector import inject
from pdip.cqrs import ICommandHandler, Dispatcher
from pdip.data.repository import RepositoryProvider
from pdip.integrator.domain.enums import StatusTypes
from pdip.integrator.domain.enums.events import EVENT_EXECUTION_FINISHED
from pdip.logging.loggers.sql import SqlLogger

from process.application.Events.ExecuteOperationFinish.ExecuteOperationFinishCommand import \
    ExecuteOperationFinishCommand
from process.application.SendExecutionFinishMail.SendExecutionFinishMailCommand import SendExecutionFinishMailCommand
from process.application.operation.services.DataOperationJobExecutionService import DataOperationJobExecutionService


class ExecuteOperationFinishCommandHandler(ICommandHandler[ExecuteOperationFinishCommand]):
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

    def handle(self, command: ExecuteOperationFinishCommand):
        try:
            if command.request.Exception is not None:
                message = f'{command.request.Operation.Id}-{command.request.Operation.Name} finished with error.'
                self.logger.exception(command.request.Exception, message, job_id=command.request.Operation.Execution.Id)
                self.__event(
                    data_operation_job_execution_id=command.request.Operation.Execution.Id,
                    status=StatusTypes.Error,
                    event_code=EVENT_EXECUTION_FINISHED
                )
            else:
                message = f'{command.request.Operation.Id}-{command.request.Operation.Name} finished.'
                self.logger.info(message, job_id=command.request.Operation.Execution.Id)
                self.__event(
                    data_operation_job_execution_id=command.request.Operation.Execution.Id,
                    status=StatusTypes.Finish,
                    event_code=EVENT_EXECUTION_FINISHED
                )
        except Exception as ex:
            self.logger.exception(ex, str(ex))
            raise Exception(str(ex))

    def __event(self,
                data_operation_job_execution_id,
                status: StatusTypes,
                event_code: int
                ):
        self.data_operation_job_execution_service.create_event(
            data_operation_execution_id=data_operation_job_execution_id,
            event_code=event_code
        )
        self.data_operation_job_execution_service.update_status(
            data_operation_job_execution_id=data_operation_job_execution_id,
            status_id=status.value,
            is_finished=True
        )

        command = SendExecutionFinishMailCommand(DataOperationJobExecutionId=data_operation_job_execution_id)
        self.dispatcher.dispatch(command)
