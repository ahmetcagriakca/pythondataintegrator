from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.connection.CreateConnectionQueue.CreateConnectionQueueRequest import CreateConnectionQueueRequest


@dataclass
class CreateConnectionQueueCommand(ICommand):
    request: CreateConnectionQueueRequest = None
