from injector import inject
from domain.connection.CreateConnectionQueue.CreateConnectionQueueCommand import CreateConnectionQueueCommand
from domain.connection.CreateConnectionQueue.CreateConnectionQueueRequest import CreateConnectionQueueRequest
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher


@controller()
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
