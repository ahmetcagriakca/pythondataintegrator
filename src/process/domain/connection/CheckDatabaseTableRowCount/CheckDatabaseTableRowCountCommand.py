from dataclasses import dataclass

from domain.connection.CheckDatabaseTableRowCount.CheckDatabaseTableRowCountRequest import CheckDatabaseTableRowCountRequest
from infrastructure.cqrs.ICommand import ICommand


@dataclass
class CheckDatabaseTableRowCountCommand(ICommand):
    request: CheckDatabaseTableRowCountRequest = None
