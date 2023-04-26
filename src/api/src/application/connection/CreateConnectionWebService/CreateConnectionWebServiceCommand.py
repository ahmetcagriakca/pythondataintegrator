from dataclasses import dataclass

from pdip.cqrs import ICommand

from src.application.connection.CreateConnectionWebService.CreateConnectionWebServiceRequest import \
    CreateConnectionWebServiceRequest


@dataclass
class CreateConnectionWebServiceCommand(ICommand):
    request: CreateConnectionWebServiceRequest = None
