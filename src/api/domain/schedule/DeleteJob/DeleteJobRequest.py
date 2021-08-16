from dataclasses import dataclass
from infrastructure.cqrs.ICommand import ICommand


@dataclass
class DeleteJobRequest(ICommand):
    Id: int = None
