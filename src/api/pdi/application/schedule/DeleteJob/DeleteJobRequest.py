from dataclasses import dataclass
from pdip.cqrs import ICommand


@dataclass
class DeleteJobRequest(ICommand):
    Id: int = None
