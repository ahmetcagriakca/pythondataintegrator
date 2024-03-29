from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.Events.ExecuteOperationIntegrationStart.ExecuteOperationIntegrationStartRequest import \
    ExecuteOperationIntegrationStartRequest


@dataclass
class ExecuteOperationIntegrationStartCommand(ICommand):
    request: ExecuteOperationIntegrationStartRequest = None
