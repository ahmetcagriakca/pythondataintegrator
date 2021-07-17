from dataclasses import dataclass
from infrastructure.cqrs.ICommand import ICommand


@dataclass
class DeleteDataOperationCommand(ICommand):
    Id: int = None
