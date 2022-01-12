from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.connection.CreateConnectionBigData.CreateConnectionBigDataRequest import \
    CreateConnectionBigDataRequest


@dataclass
class CreateConnectionBigDataCommand(ICommand):
    request: CreateConnectionBigDataRequest = None
