from dataclasses import dataclass
from pdip.cqrs import ICommand


@dataclass
class CreateExecutionCommand(ICommand):
    DataOperationId: int = None
    JobId: int = None
