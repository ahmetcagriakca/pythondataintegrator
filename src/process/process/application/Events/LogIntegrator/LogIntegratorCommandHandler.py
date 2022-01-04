from injector import inject
from pdip.cqrs import ICommandHandler, Dispatcher
from pdip.data.repository import RepositoryProvider
from pdip.integrator.operation.domain import OperationBase
from pdip.logging.loggers.sql import SqlLogger

from process.application.Events.LogIntegrator.LogIntegratorCommand import LogIntegratorCommand


class LogIntegratorCommandHandler(ICommandHandler[LogIntegratorCommand]):
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

    def handle(self, command: LogIntegratorCommand):
        try:

            if command.request.Exception is not None:
                if isinstance(command.request.Data, OperationBase):
                    log_message = f'{command.request.Data.Id}-{command.request.Data.Name}-{command.request.Message}'
                else:
                    log_message = f'{command.request.Data.Id}-{command.request.Data.Order}-{command.request.Data.Name}-{command.request.Message}'

                self.logger.exception(command.request.Exception, log_message)
            else:
                if isinstance(command.request.Data, OperationBase):
                    log_message = f'{command.request.Data.Id}-{command.request.Data.Name}-{command.request.Message}'
                else:
                    log_message = f'{command.request.Data.Id}-{command.request.Data.Order}-{command.request.Data.Name}-{command.request.Message}'
                self.logger.info(log_message)
        except Exception as ex:
            self.logger.exception(ex, str(ex))
            raise Exception(str(ex))
