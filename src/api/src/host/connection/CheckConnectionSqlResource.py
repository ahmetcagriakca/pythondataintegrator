from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from src.application.connection.CheckSqlConnection.CheckSqlConnectionCommand import \
    CheckSqlConnectionCommand
from src.application.connection.CheckSqlConnection.CheckSqlConnectionRequest import \
    CheckSqlConnectionRequest


class CheckConnectionSqlResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: CheckSqlConnectionRequest):
        """
        Check Database Connection
        """
        command = CheckSqlConnectionCommand(request=req)
        self.dispatcher.dispatch(command)
