from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.connection.DeleteConnection.DeleteConnectionRequest import DeleteConnectionRequest


@dataclass
class DeleteConnectionCommand(ICommand):
    request: DeleteConnectionRequest = None
