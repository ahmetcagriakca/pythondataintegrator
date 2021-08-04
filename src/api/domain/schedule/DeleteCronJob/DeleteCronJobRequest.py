from dataclasses import dataclass
from infrastructure.cqrs.ICommand import ICommand


@dataclass
class DeleteCronJobRequest(ICommand):
    OperationName: str = None
