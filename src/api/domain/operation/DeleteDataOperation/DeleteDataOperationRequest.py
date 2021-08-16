from dataclasses import dataclass
from infrastructure.cqrs.ICommand import ICommand


@dataclass
class DeleteDataOperationRequest:
    Id: int = None
