from dataclasses import dataclass
from pdip.cqrs import ICommand

from pdi.application.operation.CreateDataOperation.CreateDataOperationRequest import CreateDataOperationRequest


@dataclass
class CreateDataOperationCommand(ICommand):
    request: CreateDataOperationRequest = None
