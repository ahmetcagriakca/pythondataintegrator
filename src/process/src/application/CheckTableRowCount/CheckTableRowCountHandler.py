from injector import inject
from pdip.cqrs import Dispatcher, ICommandHandler
from pdip.data.decorators import transactionhandler
from pdip.integrator.connection.domain.enums import ConnectionTypes
from pdip.integrator.connection.types.bigdata.base import BigDataProvider
from pdip.integrator.connection.types.sql.base import SqlProvider
from pdip.logging.loggers.sql import SqlLogger
from pyodbc import ProgrammingError

from src.application.CheckTableRowCount.CheckTableRowCountCommand import \
    CheckTableRowCountCommand
from src.application.SendNotification.SendNotificationCommand import SendNotificationCommand
from src.application.SendNotification.SendNotificationRequest import SendNotificationRequest
from src.application.integrator.OperationCacheService import OperationCacheService
from src.application.integrator.converters.ConnectionConverter import ConnectionConverter


class CheckTableRowCountHandler(ICommandHandler[CheckTableRowCountCommand]):
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
    def handle(self, command: CheckTableRowCountCommand):
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
        count_of_table = ''
        schema = command.request.Schema
        table = command.request.Table
        if schema is not None and schema != '' and table is not None and table != '':
            try:
                count_query = context.dialect.get_table_select_query(selected_rows='1 first_column',
                                                                       schema=schema,
                                                                       table=table)
                count = context.get_table_count(query=count_query)
                count_of_table = f'"{schema}"."{table}" has {count} row'
            except Exception as ex:
                message = f'{connection.Name} "{schema}"."{table}" count of table getting error! Error: {ex}'
                self.logger.exception(ex, message)
                raise Exception(str(ex))
            except any as ex:
                raise Exception(str(ex))
        self.notify(message=f'{connection.Name} connected. {count_of_table}')

    def notify(self, message: str):
        send_notification_request = SendNotificationRequest(Message=message,
                                                            Type=1)
        self.dispatcher.dispatch(SendNotificationCommand(request=send_notification_request))
