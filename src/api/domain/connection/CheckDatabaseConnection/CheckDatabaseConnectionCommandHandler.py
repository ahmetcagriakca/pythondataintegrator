from injector import inject

from domain.connection.CheckDatabaseConnection.CheckDatabaseConnectionCommand import CheckDatabaseConnectionCommand
from infrastructure.cqrs.ICommandHandler import ICommandHandler
from infrastructure.exceptions.OperationalException import OperationalException
from rpc.ProcessRpcClientService import ProcessRpcClientService


class CheckDatabaseConnectionCommandHandler(ICommandHandler[CheckDatabaseConnectionCommand]):
    @inject
    def __init__(self, process_rpc_client_service: ProcessRpcClientService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process_rpc_client_service = process_rpc_client_service

    def handle(self, command: CheckDatabaseConnectionCommand):
        result = self.process_rpc_client_service.call_check_database_connection(connection_name=command.ConnectionName)
        if result != 'Connected successfully. ':
            raise OperationalException(result)
