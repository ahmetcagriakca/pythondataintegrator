from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from src.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionQuery import \
    GetDataOperationJobExecutionQuery
from src.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionRequest import \
    GetDataOperationJobExecutionRequest
from src.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionResponse import \
    GetDataOperationJobExecutionResponse
from src.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListQuery import \
    GetDataOperationJobExecutionListQuery
from src.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListRequest import \
    GetDataOperationJobExecutionListRequest
from src.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListResponse import \
    GetDataOperationJobExecutionListResponse


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
