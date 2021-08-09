import json

from injector import inject
import requests
from domain.notification.SendNotification.SendNotificationCommand import SendNotificationCommand
from infrastructure.cqrs.ICommandHandler import ICommandHandler
from infrastructure.json.DateTimeEncoder import DateTimeEncoder
from infrastructure.logging.SqlLogger import SqlLogger


class SendNotificationCommandHandler(ICommandHandler[SendNotificationCommand]):
    @inject
    def __init__(self,
                 logger: SqlLogger,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger

    def handle(self, command: SendNotificationCommand):
        try:
            url = 'http://localhost:7500/notify'
            data = json.dumps(command.request.to_dict(), cls=DateTimeEncoder, indent=4)
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            response = requests.post(url, json=data, headers=headers)
        except Exception as e:
            self.logger.exception(exception=e, message="Send Notifiaction getting error.")
