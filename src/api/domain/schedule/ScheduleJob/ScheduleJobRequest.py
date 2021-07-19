from datetime import datetime

from domain.common.decorators.requestclass import requestclass


@requestclass
class ScheduleJobRequest:
    OperationName: str = None
    RunDate: datetime = None
