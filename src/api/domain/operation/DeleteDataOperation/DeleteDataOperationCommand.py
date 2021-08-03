from dataclasses import dataclass

from domain.operation.DeleteDataOperation.DeleteDataOperationRequest import DeleteDataOperationRequest
from infrastructure.cqrs.ICommand import ICommand


@dataclass
class DeleteDataOperationCommand(ICommand):
    request: DeleteDataOperationRequest = None
