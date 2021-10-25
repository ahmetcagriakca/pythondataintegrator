from dataclasses import dataclass

from domain.operation.DeleteDataOperation.DeleteDataOperationRequest import DeleteDataOperationRequest
from pdip.cqrs import ICommand


@dataclass
class DeleteDataOperationCommand(ICommand):
    request: DeleteDataOperationRequest = None
