from dataclasses import dataclass
from pdip.cqrs import ICommand


@dataclass
class SendSchedulerErrorMailCommand(ICommand):
    JobId: int = None
    DataOperationJobExecutionId: int = None
    Exception: Exception = None
