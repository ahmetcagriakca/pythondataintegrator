from dataclasses import dataclass

from process.application.SendNotification.SendNotificationRequest import SendNotificationRequest
from pdip.cqrs import ICommand


@dataclass
class SendNotificationCommand(ICommand):
    request: SendNotificationRequest = None
