from typing import List

from pdip.cqrs.decorators import requestclass


@requestclass
class RescheduleCronJobsRequest:
    DataOperationNames: List[str] = None
