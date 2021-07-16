from dataclasses import dataclass
from infrastructure.cqrs.ICommand import ICommand

@dataclass
class DeleteConnectionCommand(ICommand):
    Id: int = None
