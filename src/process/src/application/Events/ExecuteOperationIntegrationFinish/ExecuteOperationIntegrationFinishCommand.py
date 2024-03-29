from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.Events.ExecuteOperationIntegrationFinish.ExecuteOperationIntegrationFinishRequest import \
    ExecuteOperationIntegrationFinishRequest


@dataclass
class ExecuteOperationIntegrationFinishCommand(ICommand):
    request: ExecuteOperationIntegrationFinishRequest = None
