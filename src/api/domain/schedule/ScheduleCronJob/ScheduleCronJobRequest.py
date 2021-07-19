from datetime import datetime

from domain.common.decorators.requestclass import requestclass


@requestclass
class ScheduleCronJobRequest:
    OperationName: str = None
    Cron: str = None
    StartDate: datetime = None
    EndDate: datetime = None
