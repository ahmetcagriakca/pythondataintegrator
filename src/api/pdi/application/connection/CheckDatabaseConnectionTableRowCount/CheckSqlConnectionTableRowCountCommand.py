from dataclasses import dataclass
from pdip.cqrs import ICommand

from pdi.application.connection.CheckDatabaseConnectionTableRowCount.CheckSqlConnectionTableRowCountRequest import \
    CheckSqlConnectionTableRowCountRequest


@dataclass
class CheckSqlConnectionTableRowCountCommand(ICommand):
    request: CheckSqlConnectionTableRowCountRequest = None
