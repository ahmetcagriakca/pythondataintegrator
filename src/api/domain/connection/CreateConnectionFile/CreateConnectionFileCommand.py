from dataclasses import dataclass
from pdip.cqrs import ICommand
from domain.connection.CreateConnectionFile.CreateConnectionFileRequest import CreateConnectionFileRequest


@dataclass
class CreateConnectionFileCommand(ICommand):
    request: CreateConnectionFileRequest = None
