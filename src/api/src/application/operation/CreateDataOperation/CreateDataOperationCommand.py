from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.operation.CreateDataOperation.CreateDataOperationRequest import CreateDataOperationRequest


@dataclass
class CreateDataOperationCommand(ICommand):
    request: CreateDataOperationRequest = None
