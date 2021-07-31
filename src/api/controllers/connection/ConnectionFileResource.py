from injector import inject
from domain.connection.CreateConnectionFile.CreateConnectionFileCommand import CreateConnectionFileCommand
from domain.connection.CreateConnectionFile.CreateConnectionFileRequest import CreateConnectionFileRequest
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher


@controller()
class ConnectionFileResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: CreateConnectionFileRequest):
        """
        Create New File Connection
        """
        command = CreateConnectionFileCommand(request=req)
        self.dispatcher.dispatch(command)
