from dataclasses import dataclass
from pdip.cqrs import ICommand

from pdi.application.operation.DeleteDataOperation.DeleteDataOperationRequest import DeleteDataOperationRequest


@dataclass
class DeleteDataOperationCommand(ICommand):
    request: DeleteDataOperationRequest = None
