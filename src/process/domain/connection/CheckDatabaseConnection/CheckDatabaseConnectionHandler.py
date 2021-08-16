from injector import inject

from domain.connection.CheckDatabaseConnection.CheckDatabaseConnectionCommand import CheckDatabaseConnectionCommand
from domain.notification.SendNotification.SendNotificationCommand import SendNotificationCommand
from domain.notification.SendNotification.SendNotificationRequest import SendNotificationRequest
from domain.operation.execution.services.OperationCacheService import OperationCacheService
from infrastructure.connection.database.DatabaseProvider import DatabaseProvider
from infrastructure.cqrs.Dispatcher import Dispatcher
from infrastructure.cqrs.ICommandHandler import ICommandHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.logging.SqlLogger import SqlLogger
from models.dao.connection import Connection


class CheckDatabaseConnectionHandler(ICommandHandler[CheckDatabaseConnectionCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 sql_logger:SqlLogger,
                 repository_provider: RepositoryProvider,
                 operation_cache_service:OperationCacheService,
                 database_provider:DatabaseProvider,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database_provider = database_provider
        self.sql_logger = sql_logger
        self.operation_cache_service = operation_cache_service
        self.repository_provider = repository_provider
        self.dispatcher = dispatcher

    def handle(self, command: CheckDatabaseConnectionCommand):
        connection = self.repository_provider.get(Connection).first(IsDeleted=0, Name=command.request.ConnectionName)
        if connection is None:
            return "Connection not found!"
        self.operation_cache_service.initialize_connection(connection.Id)
        database_context = self.database_provider.get_context(connection=connection)
        database_context.connector.connect()
        self.notify(message=f'{command.request.ConnectionName} connected successfully.')

    def notify(self, message: str):
        send_notification_request = SendNotificationRequest(Message=message,
                                                            Type=1)
        self.dispatcher.dispatch(SendNotificationCommand(request=send_notification_request))
