from domain.operation.GetDataOperationJobList.GetDataOperationJobListRequest import GetDataOperationJobListRequest
from domain.operation.GetDataOperationJobList.GetDataOperationJobListResponse import GetDataOperationJobListResponse
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher

from injector import inject
from infrastructure.api.ResourceBase import ResourceBase


@controller()
class OperationJobResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: GetDataOperationJobListRequest) -> GetDataOperationJobListResponse:
        """
        Get All Data Operation Jobs
        """
        query = GetDataOperationJobListRequest(request=req)
        result = self.dispatcher.dispatch(query)
        return result

