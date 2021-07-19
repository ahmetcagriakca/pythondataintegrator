from injector import inject
from domain.operation.LookupDataOperation.LookupDataOperationQuery import LookupDataOperationQuery
from domain.operation.LookupDataOperation.LookupDataOperationRequest import LookupDataOperationRequest
from domain.operation.LookupDataOperation.LookupDataOperationResponse import LookupDataOperationResponse
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher


@controller()
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
