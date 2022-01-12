from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.Events.ExecuteOperationStart.ExecuteOperationStartRequest import \
    ExecuteOperationStartRequest


@dataclass
class ExecuteOperationStartCommand(ICommand):
    request: ExecuteOperationStartRequest = None
