from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from src.application.connection.CreateConnectionSql.CreateConnectionSqlCommand import \
    CreateConnectionSqlCommand
from src.application.connection.CreateConnectionSql.CreateConnectionSqlRequest import \
    CreateConnectionSqlRequest


class ConnectionSqlResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: CreateConnectionSqlRequest):
        """
        Create New Database Connection
        """
        command = CreateConnectionSqlCommand(request=req)
        self.dispatcher.dispatch(command)
