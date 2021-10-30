from injector import inject
from pdip.cqrs import Dispatcher, ICommandHandler
from pdip.exceptions import OperationalException

from pdi.application.connection.CheckDatabaseConnectionTableRowCount.CheckDatabaseConnectionTableRowCountCommand import \
    CheckDatabaseConnectionTableRowCountCommand
from pdi.application.rpc.clients.ProcessRpcClientService import ProcessRpcClientService


class CheckDatabaseConnectionTableRowCountCommandHandler(ICommandHandler[CheckDatabaseConnectionTableRowCountCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 process_rpc_client_service: ProcessRpcClientService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher
        self.process_rpc_client_service = process_rpc_client_service

    def handle(self, command: CheckDatabaseConnectionTableRowCountCommand):
        try:
            self.process_rpc_client_service.call_check_database_table_row_count(
                connection_name=command.request.ConnectionName,
                schema=command.request.Schema,
                table=command.request.Table,
            )
        except Exception as ex:
            message = f'{command.request.ConnectionName} getting error on checking count. Error:{ex.args[len(ex.args) - 1]}'
            raise OperationalException(message)
