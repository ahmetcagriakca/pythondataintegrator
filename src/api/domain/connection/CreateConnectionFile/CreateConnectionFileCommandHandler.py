from injector import inject
from domain.connection.CreateConnectionFile.CreateConnectionFileCommand import CreateConnectionFileCommand
from domain.connection.services.ConnectionService import ConnectionService
from infrastructure.cqrs.ICommandHandler import ICommandHandler


class CreateConnectionFileCommandHandler(ICommandHandler[CreateConnectionFileCommand]):
    @inject
    def __init__(self,
                 connection_service: ConnectionService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_service = connection_service

    def handle(self, command: CreateConnectionFileCommand):
        self.connection_service.create_connection_file(command.request)
