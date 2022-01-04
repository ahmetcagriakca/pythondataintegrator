from dataclasses import dataclass
from pdip.cqrs import ICommand

from process.application.Events.ExecuteOperationInitialize.ExecuteOperationInitializeRequest import ExecuteOperationInitializeRequest


@dataclass
class ExecuteOperationInitializeCommand(ICommand):
    request: ExecuteOperationInitializeRequest = None
