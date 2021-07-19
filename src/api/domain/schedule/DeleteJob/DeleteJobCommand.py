from dataclasses import dataclass
from infrastructure.cqrs.ICommand import ICommand


@dataclass
class DeleteJobCommand(ICommand):
    Id: int = None
