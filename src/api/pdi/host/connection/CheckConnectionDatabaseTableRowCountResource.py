from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from pdi.application.connection.CheckDatabaseConnectionTableRowCount.CheckDatabaseConnectionTableRowCountCommand import \
    CheckDatabaseConnectionTableRowCountCommand
from pdi.application.connection.CheckDatabaseConnectionTableRowCount.CheckDatabaseConnectionTableRowCountRequest import \
    CheckDatabaseConnectionTableRowCountRequest


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
