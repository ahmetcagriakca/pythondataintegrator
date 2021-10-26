from dataclasses import dataclass
from pdip.cqrs import ICommand


@dataclass
class SendMissMailCommand(ICommand):
    JobId: int = None
