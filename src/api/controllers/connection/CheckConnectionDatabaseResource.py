from injector import inject

from domain.connection.CheckDatabaseConnection.CheckDatabaseConnectionCommand import CheckDatabaseConnectionCommand
from domain.connection.CheckDatabaseConnection.CheckDatabaseConnectionRequest import CheckDatabaseConnectionRequest
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher


@controller()
class CheckConnectionDatabaseResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: CheckDatabaseConnectionRequest):
        """
        Check Database Connection
        """
        command = CheckDatabaseConnectionCommand(request=req)
        self.dispatcher.dispatch(command)