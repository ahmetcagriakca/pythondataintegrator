from dataclasses import dataclass
from pdip.cqrs import ICommand

from pdi.application.notification.SendNotification.SendNotificationRequest import SendNotificationRequest


@dataclass
class SendNotificationCommand(ICommand):
    request: SendNotificationRequest = None
