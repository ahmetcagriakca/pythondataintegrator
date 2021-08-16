from dataclasses import dataclass

from domain.connection.CreateConnectionDatabase.CreateConnectionDatabaseRequest import CreateConnectionDatabaseRequest
from infrastructure.cqrs.ICommand import ICommand


@dataclass
class CreateConnectionDatabaseCommand(ICommand):
    request: CreateConnectionDatabaseRequest = None
