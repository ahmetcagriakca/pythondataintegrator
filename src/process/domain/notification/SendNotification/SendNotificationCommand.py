from dataclasses import dataclass

from domain.notification.SendNotification.SendNotificationRequest import SendNotificationRequest
from infrastructure.cqrs.ICommand import ICommand


@dataclass
class SendNotificationCommand(ICommand):
    request: SendNotificationRequest = None
