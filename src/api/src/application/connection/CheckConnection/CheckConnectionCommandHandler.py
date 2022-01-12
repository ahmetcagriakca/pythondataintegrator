from injector import inject
from pdip.cqrs import Dispatcher
from pdip.cqrs import ICommandHandler
from pdip.exceptions import OperationalException

from src.application.connection.CheckConnection.CheckConnectionCommand import \
    CheckConnectionCommand
from src.application.rpc.clients.ProcessRpcClientService import ProcessRpcClientService


class CheckConnectionCommandHandler(ICommandHandler[CheckConnectionCommand]):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 process_rpc_client_service: ProcessRpcClientService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher
        self.process_rpc_client_service = process_rpc_client_service

    def handle(self, command: CheckConnectionCommand):
        try:
            self.process_rpc_client_service.call_check_connection(connection_id=command.request.ConnectionId)
        except ConnectionRefusedError as cre:
            error_detail = str(cre)
            message = f'{command.request.ConnectionId} getting error on connecting. Process machine is not accessible. Error:{error_detail}'
            raise OperationalException(message)
        except Exception as ex:
            error_detail = str(ex)
            message = f'{command.request.ConnectionId} getting error on connecting. Error:{error_detail}'
            raise OperationalException(message)
