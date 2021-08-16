from dataclasses import dataclass
from infrastructure.cqrs.ICommand import ICommand
from domain.connection.CreateConnectionFile.CreateConnectionFileRequest import CreateConnectionFileRequest


@dataclass
class CreateConnectionFileCommand(ICommand):
    request: CreateConnectionFileRequest = None
