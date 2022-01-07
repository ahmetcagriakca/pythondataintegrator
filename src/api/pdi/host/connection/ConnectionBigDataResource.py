from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from pdi.application.connection.CreateConnectionBigData.CreateConnectionBigDataCommand import \
    CreateConnectionBigDataCommand
from pdi.application.connection.CreateConnectionBigData.CreateConnectionBigDataRequest import \
    CreateConnectionBigDataRequest


class ConnectionBigDataResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: CreateConnectionBigDataRequest):
        """
        Create New Database Connection
        """
        command = CreateConnectionBigDataCommand(request=req)
        self.dispatcher.dispatch(command)
