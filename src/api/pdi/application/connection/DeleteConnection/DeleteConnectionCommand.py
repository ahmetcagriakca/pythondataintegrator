from dataclasses import dataclass
from pdip.cqrs import ICommand

from pdi.application.connection.DeleteConnection.DeleteConnectionRequest import DeleteConnectionRequest


@dataclass
class DeleteConnectionCommand(ICommand):
    request: DeleteConnectionRequest = None
