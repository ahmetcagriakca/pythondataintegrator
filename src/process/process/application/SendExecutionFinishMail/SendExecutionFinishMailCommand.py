from dataclasses import dataclass
from pdip.cqrs import ICommand


@dataclass
class SendExecutionFinishMailCommand(ICommand):
    DataOperationJobExecutionId: int = None
