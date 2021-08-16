from datetime import datetime

from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class ScheduleJobRequest:
    OperationName: str = None
    RunDate: datetime = None
