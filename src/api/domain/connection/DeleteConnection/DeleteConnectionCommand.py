from dataclasses import dataclass

from domain.connection.DeleteConnection.DeleteConnectionRequest import DeleteConnectionRequest
from pdip.cqrs import ICommand

@dataclass
class DeleteConnectionCommand(ICommand):
    request:DeleteConnectionRequest=None
