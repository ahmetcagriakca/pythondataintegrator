from injector import inject

from domain.connection.CheckDatabaseTableRowCount.CheckDatabaseTableRowCountCommand import \
    CheckDatabaseTableRowCountCommand
from domain.notification.SendNotification.SendNotificationCommand import SendNotificationCommand
from domain.notification.SendNotification.SendNotificationRequest import SendNotificationRequest
from domain.operation.execution.services.OperationCacheService import OperationCacheService
from infrastructure.connection.database.DatabaseProvider import DatabaseProvider
from infrastructure.cqrs.Dispatcher import Dispatcher
from infrastructure.cqrs.ICommandHandler import ICommandHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.logging.SqlLogger import SqlLogger
from models.dao.connection import Connection


class CheckDatabaseTableRowCountHandler(ICommandHandler[CheckDatabaseTableRowCountCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 logger: SqlLogger,
                 repository_provider: RepositoryProvider,
                 operation_cache_service: OperationCacheService,
                 database_provider: DatabaseProvider,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database_provider = database_provider
        self.logger = logger
        self.operation_cache_service = operation_cache_service
        self.repository_provider = repository_provider
        self.dispatcher = dispatcher

    def handle(self, command: CheckDatabaseTableRowCountCommand):
        connection = self.repository_provider.get(Connection).first(IsDeleted=0, Name=command.request.ConnectionName)
        if connection is None:
            return "Connection not found!"
        self.operation_cache_service.initialize_connection(connection.Id)
        database_context = self.database_provider.get_context(connection=connection)
        database_context.connector.connect()
        database_context.connector.disconnect()
        count_of_table = ''
        schema = command.request.Schema
        table = command.request.Table
        if schema is not None and schema != '' and table is not None and table != '':
            try:
                count = database_context.get_table_count(f'select * from "{schema}"."{table}"')
                count_of_table = f'"{schema}"."{table}" has {count} row'
            except Exception as ex:
                message = f'{command.request.ConnectionName} "{schema}"."{table}" count of table getting error! Error: {ex}'
                self.logger.exception(ex, message)
                raise
        self.notify(message=f'{command.request.ConnectionName} connected. {count_of_table}')

    def notify(self, message: str):
        send_notification_request = SendNotificationRequest(Message=message,
                                                            Type=1)
        self.dispatcher.dispatch(SendNotificationCommand(request=send_notification_request))
