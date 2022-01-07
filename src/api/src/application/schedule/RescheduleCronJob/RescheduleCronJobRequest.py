from typing import List

from pdip.cqrs.decorators import requestclass


@requestclass
class RescheduleCronJobRequest:
    DataOperationName: str = None
