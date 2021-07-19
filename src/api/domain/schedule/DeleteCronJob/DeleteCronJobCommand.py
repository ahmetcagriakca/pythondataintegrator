from dataclasses import dataclass
from infrastructure.cqrs.ICommand import ICommand


@dataclass
class DeleteCronJobCommand(ICommand):
    DataOperationName: str = None
