from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from pdi.application.connection.CreateConnectionDatabase.CreateConnectionDatabaseCommand import \
    CreateConnectionDatabaseCommand
from pdi.application.connection.CreateConnectionDatabase.CreateConnectionDatabaseRequest import \
    CreateConnectionDatabaseRequest


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
