from injector import inject

from domain.connection.CreateConnectionDatabase.CreateConnectionDatabaseCommand import CreateConnectionDatabaseCommand
from domain.connection.services.ConnectionService import ConnectionService
from infrastructure.cqrs.ICommandHandler import ICommandHandler


class CreateConnectionDatabaseCommandHandler(ICommandHandler[CreateConnectionDatabaseCommand]):
    @inject
    def __init__(self,
                 connection_service: ConnectionService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_service = connection_service

    def handle(self, command: CreateConnectionDatabaseCommand):
        self.connection_service.create_connection_database(command.request)
