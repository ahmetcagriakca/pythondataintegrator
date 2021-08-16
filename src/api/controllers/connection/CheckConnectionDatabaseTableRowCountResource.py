from injector import inject

from domain.connection.CheckDatabaseConnectionTableRowCount.CheckDatabaseConnectionTableRowCountCommand import \
    CheckDatabaseConnectionTableRowCountCommand
from domain.connection.CheckDatabaseConnectionTableRowCount.CheckDatabaseConnectionTableRowCountRequest import \
    CheckDatabaseConnectionTableRowCountRequest
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher


@controller()
class CheckConnectionDatabaseTableRowCountResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: CheckDatabaseConnectionTableRowCountRequest):
        """
        Check Database Connection
        """
        command = CheckDatabaseConnectionTableRowCountCommand(request=req)
        self.dispatcher.dispatch(command)