from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from pdi.application.connection.GetConnectionBigData.GetConnectionBigDataQuery import GetConnectionBigDataQuery
from pdi.application.connection.GetConnectionBigData.GetConnectionBigDataRequest import GetConnectionBigDataRequest
from pdi.application.connection.GetConnectionBigData.GetConnectionBigDataResponse import GetConnectionBigDataResponse


class ConnectionBigDataByIdResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: GetConnectionBigDataRequest) -> GetConnectionBigDataResponse:
        """
        Get BigData Connection By Id
        """
        query = GetConnectionBigDataQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result
