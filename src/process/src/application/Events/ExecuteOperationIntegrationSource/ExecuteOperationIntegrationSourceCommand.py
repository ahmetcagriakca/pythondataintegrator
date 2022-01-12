from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.Events.ExecuteOperationIntegrationSource.ExecuteOperationIntegrationSourceRequest import \
    ExecuteOperationIntegrationSourceRequest
from src.application.Events.ExecuteOperationIntegrationTargetTruncate.ExecuteOperationIntegrationTargetTruncateRequest import \
    ExecuteOperationIntegrationTargetTruncateRequest


@dataclass
class ExecuteOperationIntegrationSourceCommand(ICommand):
    request: ExecuteOperationIntegrationSourceRequest = None
