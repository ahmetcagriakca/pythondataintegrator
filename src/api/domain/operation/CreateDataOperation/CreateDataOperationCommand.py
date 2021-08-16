from dataclasses import dataclass
from infrastructure.cqrs.ICommand import ICommand
from domain.operation.CreateDataOperation.CreateDataOperationRequest import CreateDataOperationRequest


@dataclass
class CreateDataOperationCommand(ICommand):
    request: CreateDataOperationRequest = None
