from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.CheckDatabaseTableRowCount.CheckDatabaseTableRowCountRequest import \
    CheckDatabaseTableRowCountRequest


@dataclass
class CheckDatabaseTableRowCountCommand(ICommand):
    request: CheckDatabaseTableRowCountRequest = None
