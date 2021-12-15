import sys

from injector import inject
from pdip.connection.database.base import DatabaseProvider
from pdip.connection.models.enums import ConnectorTypes
from pdip.cqrs import Dispatcher, ICommandHandler
from pdip.data import RepositoryProvider
from pdip.logging.loggers.database import SqlLogger

from process.application.CheckDatabaseConnection.CheckDatabaseConnectionCommand import CheckDatabaseConnectionCommand
from process.application.SendNotification.SendNotificationCommand import SendNotificationCommand
from process.application.SendNotification.SendNotificationRequest import SendNotificationRequest
from process.application.execution.services.OperationCacheService import OperationCacheService
from process.domain.connection import Connection


class CheckDatabaseConnectionHandler(ICommandHandler[CheckDatabaseConnectionCommand]):
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

    def handle(self, command: CheckDatabaseConnectionCommand):
        try:
            connection = self.repository_provider.get(Connection).first(IsDeleted=0,
                                                                        Name=command.request.ConnectionName)
            if connection is None:
                return "Connection not found!"
            self.operation_cache_service.initialize_connection(connection.Id)
            connection_basic_authentication = self.operation_cache_service.get_connection_basic_authentication_by_connection_id(
                connection_id=connection.Id)
            connection_server = self.operation_cache_service.get_connection_server_by_connection_id(
                connection_id=connection.Id)

            database_context = self.database_provider.get_context(
                connector_type=ConnectorTypes(connection.Database.ConnectorTypeId), host=connection_server.Host,
                port=connection_server.Port, user=connection_basic_authentication.User,
                password=connection_basic_authentication.Password, database=connection.Database.DatabaseName,
                service_name=connection.Database.ServiceName, sid=connection.Database.Sid)
            database_context.connector.connect()
            self.notify(message=f'{command.request.ConnectionName} connected successfully.')
        except Exception as ex:
            self.logger.exception(ex, str(ex))
            raise Exception(str(ex))

    def notify(self, message: str):
        send_notification_request = SendNotificationRequest(Message=message,
                                                            Type=1)
        self.dispatcher.dispatch(SendNotificationCommand(request=send_notification_request))