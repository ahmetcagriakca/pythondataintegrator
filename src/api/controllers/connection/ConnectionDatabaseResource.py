from injector import inject
from domain.connection.CreateConnectionDatabase.CreateConnectionDatabaseCommand import CreateConnectionDatabaseCommand
from domain.connection.CreateConnectionDatabase.CreateConnectionDatabaseRequest import CreateConnectionDatabaseRequest
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher


@controller()
class ConnectionDatabaseResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: CreateConnectionDatabaseRequest):
        """
        Create New Database Connection
        """
        command = CreateConnectionDatabaseCommand(request=req)
        self.dispatcher.dispatch(command)
        return "Connected created"
