from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from pdi.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionQuery import \
    GetDataOperationJobExecutionQuery
from pdi.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionRequest import \
    GetDataOperationJobExecutionRequest
from pdi.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionResponse import \
    GetDataOperationJobExecutionResponse
from pdi.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListQuery import \
    GetDataOperationJobExecutionListQuery
from pdi.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListRequest import \
    GetDataOperationJobExecutionListRequest
from pdi.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListResponse import \
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
