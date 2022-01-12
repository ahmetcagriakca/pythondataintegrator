from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from src.application.connection.CreateConnectionQueue.CreateConnectionQueueCommand import CreateConnectionQueueCommand
from src.application.connection.CreateConnectionQueue.CreateConnectionQueueRequest import CreateConnectionQueueRequest


class ConnectionQueueResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: CreateConnectionQueueRequest):
        """
        Create New Queue Connection
        """
        command = CreateConnectionQueueCommand(request=req)
        self.dispatcher.dispatch(command)
