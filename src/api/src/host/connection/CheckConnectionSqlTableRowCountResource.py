from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from src.application.connection.CheckDatabaseConnectionTableRowCount.CheckSqlConnectionTableRowCountCommand import \
    CheckSqlConnectionTableRowCountCommand
from src.application.connection.CheckDatabaseConnectionTableRowCount.CheckSqlConnectionTableRowCountRequest import \
    CheckSqlConnectionTableRowCountRequest


class CheckConnectionSqlTableRowCountResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: CheckSqlConnectionTableRowCountRequest):
        """
        Check Database Connection
        """
        command = CheckSqlConnectionTableRowCountCommand(request=req)
        self.dispatcher.dispatch(command)
