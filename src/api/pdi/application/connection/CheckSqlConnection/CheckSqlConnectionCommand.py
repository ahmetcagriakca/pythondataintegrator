from dataclasses import dataclass
from pdip.cqrs import ICommand

from pdi.application.connection.CheckSqlConnection.CheckSqlConnectionRequest import \
    CheckSqlConnectionRequest


@dataclass
class CheckSqlConnectionCommand(ICommand):
    request: CheckSqlConnectionRequest = None
