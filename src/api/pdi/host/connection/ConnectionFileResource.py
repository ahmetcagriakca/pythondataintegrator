from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from pdi.application.connection.CreateConnectionFile.CreateConnectionFileCommand import CreateConnectionFileCommand
from pdi.application.connection.CreateConnectionFile.CreateConnectionFileRequest import CreateConnectionFileRequest


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
