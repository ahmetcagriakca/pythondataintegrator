from dataclasses import dataclass

from domain.connection.DeleteConnection.DeleteConnectionRequest import DeleteConnectionRequest
from infrastructure.cqrs.ICommand import ICommand

@dataclass
class DeleteConnectionCommand(ICommand):
    request:DeleteConnectionRequest=None
