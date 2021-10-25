from dataclasses import dataclass
from pdip.cqrs import ICommand


@dataclass
class DeleteDataOperationRequest:
    Id: int = None
