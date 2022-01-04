from dataclasses import dataclass
from pdip.cqrs import ICommand

from process.application.Events.LogIntegrator.LogIntegratorRequest import LogIntegratorRequest


@dataclass
class LogIntegratorCommand(ICommand):
    request: LogIntegratorRequest = None
