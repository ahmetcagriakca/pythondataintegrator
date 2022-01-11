from injector import inject
from pdip.cqrs import Dispatcher, ICommandHandler
from pdip.data.decorators import transactionhandler
from pdip.integrator.connection.domain.enums import ConnectionTypes
from pdip.integrator.connection.types.bigdata.base import BigDataProvider
from pdip.integrator.connection.types.sql.base import SqlProvider
from pdip.logging.loggers.sql import SqlLogger

from src.application.CheckConnection.CheckConnectionCommand import CheckConnectionCommand
from src.application.SendNotification.SendNotificationCommand import SendNotificationCommand
from src.application.SendNotification.SendNotificationRequest import SendNotificationRequest
from src.application.integrator.OperationCacheService import OperationCacheService
from src.application.integrator.converters.ConnectionConverter import ConnectionConverter


class CheckConnectionHandler(ICommandHandler[CheckConnectionCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 logger: SqlLogger,
                 operation_cache_service: OperationCacheService,
                 connection_converter: ConnectionConverter,
                 sql_provider: SqlProvider,
                 big_data_provider: BigDataProvider,
                 *args, **kwargs
                 ):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher
        self.logger = logger
        self.operation_cache_service = operation_cache_service
        self.connection_converter = connection_converter
        self.sql_provider = sql_provider
        self.big_data_provider = big_data_provider

    @transactionhandler
    def handle(self, command: CheckConnectionCommand):
        connection = self.operation_cache_service.initialize_connection(command.request.ConnectionId)
        if connection.ConnectionType.Id == ConnectionTypes.Sql.value:
            connection_config = self.connection_converter.convert_connection_sql(connection=connection)
            context = self.sql_provider.get_context_by_config(connection_config)
        elif connection.ConnectionType.Id == ConnectionTypes.BigData.value:
            connection_config = self.connection_converter.convert_connection_big_data(connection=connection)
            context = self.big_data_provider.get_context_by_config(connection_config)

        try:
            context.connector.connect()
            context.connector.disconnect()
        except Exception as ex:
            raise Exception(str(ex))

        self.notify(message=f'{connection.Name} connected successfully.')

    def notify(self, message: str):
        send_notification_request = SendNotificationRequest(Message=message,
                                                            Type=1)
        self.dispatcher.dispatch(SendNotificationCommand(request=send_notification_request))
