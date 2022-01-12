from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from src.application.connection.CheckConnection.CheckConnectionCommand import \
    CheckConnectionCommand
from src.application.connection.CheckConnection.CheckConnectionRequest import \
    CheckConnectionRequest


class CheckConnectionResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: CheckConnectionRequest):
        """
        Check Database Connection
        """
        command = CheckConnectionCommand(request=req)
        self.dispatcher.dispatch(command)
