from injector import inject
from domain.connection.CreateConnectionQueue.CreateConnectionQueueCommand import CreateConnectionQueueCommand
from domain.connection.services.ConnectionService import ConnectionService
from infrastructure.cqrs.ICommandHandler import ICommandHandler


class CreateConnectionQueueCommandHandler(ICommandHandler[CreateConnectionQueueCommand]):
    @inject
    def __init__(self,
                 connection_service: ConnectionService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_service = connection_service

    def handle(self, command: CreateConnectionQueueCommand):
        self.connection_service.create_connection_queue(command.request)
