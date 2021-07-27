from domain.operation.GetDataOperationJob.GetDataOperationJobQuery import GetDataOperationJobQuery
from domain.operation.GetDataOperationJob.GetDataOperationJobRequest import GetDataOperationJobRequest
from domain.operation.GetDataOperationJob.GetDataOperationJobResponse import GetDataOperationJobResponse
from domain.operation.GetDataOperationJobList.GetDataOperationJobListQuery import GetDataOperationJobListQuery
from domain.operation.GetDataOperationJobList.GetDataOperationJobListRequest import GetDataOperationJobListRequest
from domain.operation.GetDataOperationJobList.GetDataOperationJobListResponse import GetDataOperationJobListResponse
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher

from injector import inject
from infrastructure.api.ResourceBase import ResourceBase


@controller()
class OperationJobByIdResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: GetDataOperationJobRequest) -> GetDataOperationJobResponse:
        """
        Get Data Operation Job By Id
        """
        query = GetDataOperationJobQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result


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
        query = GetDataOperationJobListQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result
