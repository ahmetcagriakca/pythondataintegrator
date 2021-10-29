from dataclasses import dataclass
from pdip.cqrs import ICommand

from pdi.application.connection.CheckDatabaseConnectionTableRowCount.CheckDatabaseConnectionTableRowCountRequest import \
    CheckDatabaseConnectionTableRowCountRequest


@dataclass
class CheckDatabaseConnectionTableRowCountCommand(ICommand):
    request: CheckDatabaseConnectionTableRowCountRequest = None
