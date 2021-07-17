from dataclasses import dataclass
from infrastructure.cqrs.ICommand import ICommand

@dataclass
class CheckDatabaseConnectionCommand(ICommand):
    ConnectionName: str = None
