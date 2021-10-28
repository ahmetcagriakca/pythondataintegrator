from dataclasses import dataclass
from pdip.cqrs import ICommand

from domain.connection.CheckDatabaseConnection.CheckDatabaseConnectionRequest import CheckDatabaseConnectionRequest


@dataclass
class CheckDatabaseConnectionCommand(ICommand):
    request: CheckDatabaseConnectionRequest = None
