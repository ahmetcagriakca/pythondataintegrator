from datetime import datetime

from pdip.cqrs.decorators import requestclass


@requestclass
class ScheduleJobRequest:
    OperationName: str = None
    RunDate: datetime = None
