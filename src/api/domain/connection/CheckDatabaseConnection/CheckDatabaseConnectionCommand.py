from dataclasses import dataclass

from domain.connection.CheckDatabaseConnection.CheckDatabaseConnectionRequest import CheckDatabaseConnectionRequest
from infrastructure.cqrs.ICommand import ICommand

@dataclass
class CheckDatabaseConnectionCommand(ICommand):
    ConnectionName: str = None
