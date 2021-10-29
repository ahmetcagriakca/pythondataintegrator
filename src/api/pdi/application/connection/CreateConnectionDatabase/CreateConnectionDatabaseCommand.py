from dataclasses import dataclass
from pdip.cqrs import ICommand

from pdi.application.connection.CreateConnectionDatabase.CreateConnectionDatabaseRequest import \
    CreateConnectionDatabaseRequest


@dataclass
class CreateConnectionDatabaseCommand(ICommand):
    request: CreateConnectionDatabaseRequest = None
