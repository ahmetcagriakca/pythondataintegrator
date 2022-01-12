from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from src.application.connection.CheckTableRowCount.CheckTableRowCountCommand import \
    CheckTableRowCountCommand
from src.application.connection.CheckTableRowCount.CheckTableRowCountRequest import \
    CheckTableRowCountRequest


class CheckTableRowCountResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: CheckTableRowCountRequest):
        """
        Check Database Connection
        """
        command = CheckTableRowCountCommand(request=req)
        self.dispatcher.dispatch(command)
