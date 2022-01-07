from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.Events.ExecuteOperationFinish.ExecuteOperationFinishRequest import \
    ExecuteOperationFinishRequest


@dataclass
class ExecuteOperationFinishCommand(ICommand):
    request: ExecuteOperationFinishRequest = None
