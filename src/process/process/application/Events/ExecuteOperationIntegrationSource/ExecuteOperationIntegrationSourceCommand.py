from dataclasses import dataclass
from pdip.cqrs import ICommand

from process.application.Events.ExecuteOperationIntegrationSource.ExecuteOperationIntegrationSourceRequest import \
    ExecuteOperationIntegrationSourceRequest
from process.application.Events.ExecuteOperationIntegrationTargetTruncate.ExecuteOperationIntegrationTargetTruncateRequest import \
    ExecuteOperationIntegrationTargetTruncateRequest


@dataclass
class ExecuteOperationIntegrationSourceCommand(ICommand):
    request: ExecuteOperationIntegrationSourceRequest = None
