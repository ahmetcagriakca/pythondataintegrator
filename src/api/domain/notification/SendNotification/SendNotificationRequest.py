from typing import List

from domain.common.decorators.requestclass import requestclass


@requestclass
class NotificationAdditionalData:
    Key: str = None
    Value: str = None


@requestclass
class SendNotificationRequest:
    Message: str = None
    Type: int = None
    Action: int = None
    AdditionalData: List[NotificationAdditionalData] = None
