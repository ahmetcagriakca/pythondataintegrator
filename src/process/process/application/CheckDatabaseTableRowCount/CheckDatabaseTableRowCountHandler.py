from injector import inject
from pdip.connection.database.base import DatabaseProvider
from pdip.connection.models.enums import ConnectorTypes
from pdip.cqrs import Dispatcher, ICommandHandler
from pdip.data import RepositoryProvider
from pdip.logging.loggers.database import SqlLogger

from process.application.CheckDatabaseTableRowCount.CheckDatabaseTableRowCountCommand import \
    CheckDatabaseTableRowCountCommand
from process.application.SendNotification.SendNotificationCommand import SendNotificationCommand
from process.application.SendNotification.SendNotificationRequest import SendNotificationRequest
from process.application.execution.services.OperationCacheService import OperationCacheService
from process.domain.connection import Connection


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
        try:
            connection = self.repository_provider.get(Connection).first(IsDeleted=0, Name=command.request.ConnectionName)
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
            database_context.connector.disconnect()
            count_of_table = ''
            schema = command.request.Schema
            table = command.request.Table
            if schema is not None and schema != '' and table is not None and table != '':
                try:
                    count_query = database_context.connector.get_table_select_query(selected_rows='1 first_column', schema=schema,
                                                                                    table=table)
                    count = database_context.get_table_count(query=count_query)
                    count_of_table = f'"{schema}"."{table}" has {count} row'
                except Exception as ex:
                    message = f'{command.request.ConnectionName} "{schema}"."{table}" count of table getting error! Error: {ex}'
                    self.logger.exception(ex, message)
                    raise
            self.notify(message=f'{command.request.ConnectionName} connected. {count_of_table}')
        except Exception as ex:
            self.logger.exception(ex, str(ex))
            raise Exception(str(ex))

    def notify(self, message: str):
        send_notification_request = SendNotificationRequest(Message=message,
                                                            Type=1)
        self.dispatcher.dispatch(SendNotificationCommand(request=send_notification_request))
