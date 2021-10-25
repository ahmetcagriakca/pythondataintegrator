from datetime import datetime

from pdip.cqrs.decorators import requestclass


@requestclass
class ScheduleCronJobRequest:
    OperationName: str = None
    Cron: str = None
    StartDate: datetime = None
    EndDate: datetime = None
