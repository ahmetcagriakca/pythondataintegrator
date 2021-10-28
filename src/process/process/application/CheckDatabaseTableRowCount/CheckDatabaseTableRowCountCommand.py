from dataclasses import dataclass
from pdip.cqrs import ICommand

from process.application.CheckDatabaseTableRowCount.CheckDatabaseTableRowCountRequest import \
    CheckDatabaseTableRowCountRequest


@dataclass
class CheckDatabaseTableRowCountCommand(ICommand):
    request: CheckDatabaseTableRowCountRequest = None
