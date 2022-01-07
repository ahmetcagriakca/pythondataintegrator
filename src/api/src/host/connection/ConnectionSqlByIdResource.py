from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from src.application.connection.GetConnectionSql.GetConnectionSqlQuery import GetConnectionSqlQuery
from src.application.connection.GetConnectionSql.GetConnectionSqlRequest import GetConnectionSqlRequest
from src.application.connection.GetConnectionSql.GetConnectionSqlResponse import GetConnectionSqlResponse


class ConnectionSqlByIdResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: GetConnectionSqlRequest) -> GetConnectionSqlResponse:
        """
        Get Data Operation Job By Id
        """
        query = GetConnectionSqlQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result
