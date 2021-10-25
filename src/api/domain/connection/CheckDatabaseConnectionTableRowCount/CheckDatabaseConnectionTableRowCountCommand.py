from dataclasses import dataclass

from domain.connection.CheckDatabaseConnectionTableRowCount.CheckDatabaseConnectionTableRowCountRequest import CheckDatabaseConnectionTableRowCountRequest
from pdip.cqrs import ICommand


@dataclass
class CheckDatabaseConnectionTableRowCountCommand(ICommand):
    request: CheckDatabaseConnectionTableRowCountRequest = None
