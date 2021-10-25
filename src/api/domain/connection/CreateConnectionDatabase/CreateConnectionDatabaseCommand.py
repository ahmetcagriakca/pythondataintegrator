from dataclasses import dataclass

from domain.connection.CreateConnectionDatabase.CreateConnectionDatabaseRequest import CreateConnectionDatabaseRequest
from pdip.cqrs import ICommand


@dataclass
class CreateConnectionDatabaseCommand(ICommand):
    request: CreateConnectionDatabaseRequest = None
