from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from domain.connection.CheckDatabaseConnection.CheckDatabaseConnectionCommand import CheckDatabaseConnectionCommand
from domain.connection.CheckDatabaseConnection.CheckDatabaseConnectionRequest import CheckDatabaseConnectionRequest


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