from IocManager import IocManager
from domain.notification.SendNotification.SendNotificationCommand import SendNotificationCommand
from domain.notification.SendNotification.SendNotificationRequest import SendNotificationRequest
from domain.operation.execution.services.OperationCacheService import OperationCacheService
from infrastructure.connection.database.DatabaseProvider import DatabaseProvider
from infrastructure.cryptography.CryptoService import CryptoService
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.logging.SqlLogger import SqlLogger
from models.configs.ApplicationConfig import ApplicationConfig
from models.dao.connection import Connection


class CheckDatabaseConnectionCommand:
    def execute(self, connection_name=None, schema=None, table=None):

        try:
            repository_provider: RepositoryProvider = RepositoryProvider()
            connection = repository_provider.get(Connection).first(IsDeleted=0, Name=connection_name)
            if connection is None:
                return "Connection not found!"
            sql_logger = SqlLogger()
            application_config = IocManager.config_manager.get(ApplicationConfig)
            crypto_service = CryptoService(application_config=application_config)
            operation_cache_service = OperationCacheService(repository_provider=repository_provider,
                                                           crypto_service=crypto_service)
            operation_cache_service.initialize_connection(connection.Id)
            database_provider = DatabaseProvider(sql_logger=sql_logger, operation_cache_service=operation_cache_service)
            database_context = database_provider.get_context(connection=connection)
            database_context.connector.connect()
            self.notify(message=f'{command.ConnectionName} connected successfully.')

        except Exception as ex:
            raise Exception(f'Connection connecting getting error! Error: {ex}')



    def notify(self, message: str):
        send_notification_request = SendNotificationRequest(Message=message,
                                                            Type=1)
        self.dispatcher.dispatch(SendNotificationCommand(request=send_notification_request))