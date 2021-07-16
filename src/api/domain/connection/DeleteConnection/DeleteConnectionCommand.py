from dataclasses import dataclass
from infrastructor.cqrs.ICommand import ICommand

@dataclass
class DeleteConnectionCommand(ICommand):
    Id: int = None
