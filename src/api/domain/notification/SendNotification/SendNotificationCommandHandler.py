import json

from injector import inject
import requests
from domain.notification.SendNotification.SendNotificationCommand import SendNotificationCommand
from infrastructure.cqrs.ICommandHandler import ICommandHandler
from infrastructure.json.DateTimeEncoder import DateTimeEncoder
from rpc.ProcessRpcClientService import ProcessRpcClientService


class SendNotificationCommandHandler(ICommandHandler[SendNotificationCommand]):
    @inject
    def __init__(self, process_rpc_client_service: ProcessRpcClientService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process_rpc_client_service = process_rpc_client_service

    def handle(self, command: SendNotificationCommand):
        try:
            url = 'http://localhost:7500/notify'
            data = json.dumps(command.request.to_dict(), cls=DateTimeEncoder, indent=4)
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            response = requests.post(url, json=data, headers=headers)
            print(response.json())
        except Exception as e:
            pass
