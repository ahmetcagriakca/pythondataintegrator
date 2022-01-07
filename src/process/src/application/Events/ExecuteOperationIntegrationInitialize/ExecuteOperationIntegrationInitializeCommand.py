from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.Events.ExecuteOperationIntegrationInitialize.ExecuteOperationIntegrationInitializeRequest import \
    ExecuteOperationIntegrationInitializeRequest


@dataclass
class ExecuteOperationIntegrationInitializeCommand(ICommand):
    request: ExecuteOperationIntegrationInitializeRequest = None
