from dataclasses import dataclass
from pdip.cqrs import ICommand


@dataclass
class DeleteCronJobRequest(ICommand):
    OperationName: str = None
