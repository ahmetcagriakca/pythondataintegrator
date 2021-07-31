from injector import inject

from domain.connection.CheckDatabaseConnection.CheckDatabaseConnectionCommand import CheckDatabaseConnectionCommand
from domain.notification.SendNotification.SendNotificationCommand import SendNotificationCommand
from domain.notification.SendNotification.SendNotificationRequest import SendNotificationRequest
from infrastructure.cqrs.Dispatcher import Dispatcher
from infrastructure.cqrs.ICommandHandler import ICommandHandler
from rpc.ProcessRpcClientService import ProcessRpcClientService


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
        result = self.process_rpc_client_service.call_check_database_connection(connection_name=command.ConnectionName)
        self.notify(message=result, connection_name=command.ConnectionName)

    def notify(self, message: str, connection_name: str):
        type = 1
        if message != 'Connected successfully. ':
            type = 2
        send_notification_request = SendNotificationRequest(Message=f'{connection_name} {message}', Type=type)
        self.dispatcher.dispatch(SendNotificationCommand(request=send_notification_request))
