from injector import inject

from domain.connection.DeleteConnection.DeleteConnectionCommand import DeleteConnectionCommand
from domain.connection.services.ConnectionService import ConnectionService
from infrastructure.cqrs.ICommandHandler import ICommandHandler


class DeleteConnectionHandler(ICommandHandler[DeleteConnectionCommand]):
    @inject
    def __init__(self,
                 connection_service: ConnectionService):
        self.connection_service = connection_service

    def handle(self,command:DeleteConnectionCommand):
        self.connection_service.delete_connection(id=command.Id)