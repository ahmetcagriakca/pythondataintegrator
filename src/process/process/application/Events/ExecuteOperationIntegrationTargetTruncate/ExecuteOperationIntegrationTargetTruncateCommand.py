from dataclasses import dataclass
from pdip.cqrs import ICommand

from process.application.Events.ExecuteOperationIntegrationTargetTruncate.ExecuteOperationIntegrationTargetTruncateRequest import \
    ExecuteOperationIntegrationTargetTruncateRequest


@dataclass
class ExecuteOperationIntegrationTargetTruncateCommand(ICommand):
    request: ExecuteOperationIntegrationTargetTruncateRequest = None
