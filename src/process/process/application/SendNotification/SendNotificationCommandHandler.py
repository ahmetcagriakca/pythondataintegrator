import json

import requests
from injector import inject
from pdip.cqrs import ICommandHandler
from pdip.json import DateTimeEncoder
from pdip.logging.loggers.database import SqlLogger

from process.domain.configs.NotificationClientConfig import NotificationClientConfig
from process.application.SendNotification.SendNotificationCommand import SendNotificationCommand


class SendNotificationCommandHandler(ICommandHandler[SendNotificationCommand]):
    @inject
    def __init__(self,
                 logger: SqlLogger,
                 notification_client_config: NotificationClientConfig,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notification_client_config = notification_client_config
        self.logger = logger

    def handle(self, command: SendNotificationCommand):
        try:
            url = f'{self.notification_client_config.host}/notify'
            data = json.dumps(command.request.to_dict(), cls=DateTimeEncoder, indent=4)
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            response = requests.post(url, json=data, headers=headers)
        except Exception as e:
            self.logger.exception(exception=e, message="Send Notifiaction getting error.")
