from dataclasses import dataclass
from pdip.cqrs import ICommand


@dataclass
class StartJobCommand(ICommand):
    DataOperationId: int = None
    JobId: int = None
