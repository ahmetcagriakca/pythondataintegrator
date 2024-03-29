from injector import inject
from pdip.cqrs import ICommandHandler, Dispatcher
from pdip.data.repository import RepositoryProvider
from pdip.logging.loggers.sql import SqlLogger

from src.application.Events.ExecuteOperationIntegrationInitialize.ExecuteOperationIntegrationInitializeCommand import \
    ExecuteOperationIntegrationInitializeCommand


class ExecuteOperationIntegrationInitializeCommandHandler(
    ICommandHandler[ExecuteOperationIntegrationInitializeCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 logger: SqlLogger,
                 repository_provider: RepositoryProvider,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger
        self.repository_provider = repository_provider
        self.dispatcher = dispatcher

    def handle(self, command: ExecuteOperationIntegrationInitializeCommand):
        try:
            message = f'{command.request.OperationIntegration.Id}-{command.request.OperationIntegration.Order}-{command.request.OperationIntegration.Name}-{command.request.Message}'
            self.logger.info(message,job_id=command.request.OperationIntegration.Execution.OperationExecutionId)
        except Exception as ex:
            self.logger.exception(ex, str(ex))
            raise Exception(str(ex))
