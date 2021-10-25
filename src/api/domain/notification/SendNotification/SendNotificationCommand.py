from dataclasses import dataclass

from domain.notification.SendNotification.SendNotificationRequest import SendNotificationRequest
from pdip.cqrs import ICommand


@dataclass
class SendNotificationCommand(ICommand):
    request: SendNotificationRequest = None
