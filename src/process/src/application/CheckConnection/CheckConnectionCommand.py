from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.CheckConnection.CheckConnectionRequest import CheckConnectionRequest


@dataclass
class CheckConnectionCommand(ICommand):
    request: CheckConnectionRequest = None
