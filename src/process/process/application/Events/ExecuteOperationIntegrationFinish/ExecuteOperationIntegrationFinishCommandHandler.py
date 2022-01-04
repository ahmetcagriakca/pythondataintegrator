from injector import inject
from pdip.cqrs import ICommandHandler, Dispatcher
from pdip.data.repository import RepositoryProvider
from pdip.logging.loggers.sql import SqlLogger

from process.application.Events.ExecuteOperationIntegrationFinish.ExecuteOperationIntegrationFinishCommand import \
    ExecuteOperationIntegrationFinishCommand


class ExecuteOperationIntegrationFinishCommandHandler(ICommandHandler[ExecuteOperationIntegrationFinishCommand]):
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

    def handle(self, command: ExecuteOperationIntegrationFinishCommand):
        try:
            if command.request.Exception is not None:
                message = f'{command.request.OperationIntegration.Id}-{command.request.OperationIntegration.Order}-{command.request.OperationIntegration.Name}-{command.request.Message}'
                self.logger.exception(command.request.Exception, message)
            else:
                message = f'{command.request.OperationIntegration.Id}-{command.request.OperationIntegration.Order}-{command.request.OperationIntegration.Name}-{command.request.Message}'
                self.logger.info(message)
        except Exception as ex:
            self.logger.exception(ex, str(ex))
            raise Exception(str(ex))
