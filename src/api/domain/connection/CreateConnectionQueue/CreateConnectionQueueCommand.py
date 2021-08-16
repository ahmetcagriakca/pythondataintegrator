from dataclasses import dataclass
from infrastructure.cqrs.ICommand import ICommand
from domain.connection.CreateConnectionQueue.CreateConnectionQueueRequest import CreateConnectionQueueRequest


@dataclass
class CreateConnectionQueueCommand(ICommand):
    request: CreateConnectionQueueRequest = None
