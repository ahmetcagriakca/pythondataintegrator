from dataclasses import dataclass
from pdip.cqrs import ICommand

from process.application.Events.ExecuteOperationIntegrationTarget.ExecuteOperationIntegrationTargetRequest import \
    ExecuteOperationIntegrationTargetRequest


@dataclass
class ExecuteOperationIntegrationTargetCommand(ICommand):
    request: ExecuteOperationIntegrationTargetRequest = None
