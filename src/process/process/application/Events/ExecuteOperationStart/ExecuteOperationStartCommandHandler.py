from injector import inject
from pdip.cqrs import ICommandHandler, Dispatcher
from pdip.data.repository import RepositoryProvider
from pdip.logging.loggers.sql import SqlLogger

from process.application.Events.ExecuteOperationStart.ExecuteOperationStartCommand import \
    ExecuteOperationStartCommand


class ExecuteOperationStartCommandHandler(ICommandHandler[ExecuteOperationStartCommand]):
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

    def handle(self, command: ExecuteOperationStartCommand):
        try:
            message = f'{command.request.Operation.Id}-{command.request.Operation.Name} started.'
            self.logger.info(message)
        except Exception as ex:
            self.logger.exception(ex, str(ex))
            raise Exception(str(ex))
