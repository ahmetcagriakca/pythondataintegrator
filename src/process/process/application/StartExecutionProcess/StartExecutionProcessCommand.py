from dataclasses import dataclass
from pdip.cqrs import ICommand


@dataclass
class StartExecutionProcessCommand(ICommand):
    DataOperationId: int = None
    JobId: int = None
    DataOperationJobExecutionId: int = None
