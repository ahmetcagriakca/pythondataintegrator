from dataclasses import dataclass
from pdip.cqrs import ICommand

from process.application.Events.ExecuteOperationFinish.ExecuteOperationFinishRequest import \
    ExecuteOperationFinishRequest


@dataclass
class ExecuteOperationFinishCommand(ICommand):
    request: ExecuteOperationFinishRequest = None
