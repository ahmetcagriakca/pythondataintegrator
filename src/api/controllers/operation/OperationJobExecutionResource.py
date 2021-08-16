from domain.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionQuery import \
    GetDataOperationJobExecutionQuery
from domain.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionRequest import \
    GetDataOperationJobExecutionRequest
from domain.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionResponse import \
    GetDataOperationJobExecutionResponse
from domain.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListQuery import \
    GetDataOperationJobExecutionListQuery
from domain.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListRequest import \
    GetDataOperationJobExecutionListRequest
from domain.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListResponse import \
    GetDataOperationJobExecutionListResponse
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher

from injector import inject
from infrastructure.api.ResourceBase import ResourceBase


@controller()
class OperationJobExecutionByIdResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: GetDataOperationJobExecutionRequest) -> GetDataOperationJobExecutionResponse:
        """
        Get Data Operation Job By Id
        """
        query = GetDataOperationJobExecutionQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result


@controller()
class OperationJobExecutionResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: GetDataOperationJobExecutionListRequest) -> GetDataOperationJobExecutionListResponse:
        """
        Get All Data Operation Jobs
        """
        query = GetDataOperationJobExecutionListQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result
