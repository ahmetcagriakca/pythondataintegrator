from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from domain.operation.LookupDataOperation.LookupDataOperationQuery import LookupDataOperationQuery
from domain.operation.LookupDataOperation.LookupDataOperationRequest import LookupDataOperationRequest
from domain.operation.LookupDataOperation.LookupDataOperationResponse import LookupDataOperationResponse


class LookupDataOperationResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: LookupDataOperationRequest) -> LookupDataOperationResponse:
        """
        Get All Data Operations
        """
        query = LookupDataOperationQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result
