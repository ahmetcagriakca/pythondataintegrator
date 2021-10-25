from dataclasses import dataclass

from domain.connection.CheckDatabaseConnection.CheckDatabaseConnectionRequest import CheckDatabaseConnectionRequest
from pdip.cqrs import ICommand


@dataclass
class CheckDatabaseConnectionCommand(ICommand):
    request: CheckDatabaseConnectionRequest = None
