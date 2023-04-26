from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from src.application.connection.CreateConnectionWebService.CreateConnectionWebServiceCommand import \
    CreateConnectionWebServiceCommand
from src.application.connection.CreateConnectionWebService.CreateConnectionWebServiceRequest import \
    CreateConnectionWebServiceRequest


class ConnectionWebServiceResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: CreateConnectionWebServiceRequest):
        """
        Create New Database Connection
        """
        command = CreateConnectionWebServiceCommand(request=req)
        self.dispatcher.dispatch(command)
