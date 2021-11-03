from injector import inject
from pdip.cqrs import Dispatcher
from pdip.cqrs import ICommandHandler
from pdip.exceptions import OperationalException

from pdi.application.connection.CheckDatabaseConnection.CheckDatabaseConnectionCommand import \
    CheckDatabaseConnectionCommand
from pdi.application.rpc.clients.ProcessRpcClientService import ProcessRpcClientService


class CheckDatabaseConnectionCommandHandler(ICommandHandler[CheckDatabaseConnectionCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 process_rpc_client_service: ProcessRpcClientService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher
        self.process_rpc_client_service = process_rpc_client_service

    def handle(self, command: CheckDatabaseConnectionCommand):
        try:
            self.process_rpc_client_service.call_check_database_connection(
                connection_name=command.request.ConnectionName)
        except ConnectionRefusedError as cre:
            error_detail = "\n".join(cre.args)
            message = f'{command.request.ConnectionName} getting error on checking count. Process machine not accessible. Error:{error_detail}'
            raise OperationalException(message)
        except Exception as ex:
            error_detail = "\n".join(ex.args)
            message = f'{command.request.ConnectionName} getting error on connecting. Error:{error_detail}'
            raise OperationalException(message)
