from injector import inject
from pdip.cqrs import Dispatcher, ICommandHandler
from pdip.exceptions import OperationalException

from src.application.connection.CheckTableRowCount.CheckTableRowCountCommand import \
    CheckTableRowCountCommand
from src.application.rpc.clients.ProcessRpcClientService import ProcessRpcClientService


class CheckTableRowCountCommandHandler(ICommandHandler[CheckTableRowCountCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 process_rpc_client_service: ProcessRpcClientService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher
        self.process_rpc_client_service = process_rpc_client_service

    def handle(self, command: CheckTableRowCountCommand):
        try:
            self.process_rpc_client_service.call_check_table_row_count(
                connection_id=command.request.ConnectionId,
                schema=command.request.Schema,
                table=command.request.Table,
            )
        except ConnectionRefusedError as cre:
            error_detail = "\n".join(cre.args)
            message = f'{command.request.ConnectionId} getting error on checking count. Process machine is not accessible. Error:{error_detail}'
            raise OperationalException(message)
        except Exception as ex:
            error_detail = "\n".join(ex.args)
            message = f'{command.request.ConnectionId} getting error on checking count. Error:{error_detail}'
            raise OperationalException(message)
