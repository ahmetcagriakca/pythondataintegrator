from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.connection.CheckTableRowCount.CheckTableRowCountRequest import \
    CheckTableRowCountRequest


@dataclass
class CheckTableRowCountCommand(ICommand):
    request: CheckTableRowCountRequest = None
