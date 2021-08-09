from datetime import datetime

from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class ScheduleCronJobRequest:
    OperationName: str = None
    Cron: str = None
    StartDate: datetime = None
    EndDate: datetime = None
