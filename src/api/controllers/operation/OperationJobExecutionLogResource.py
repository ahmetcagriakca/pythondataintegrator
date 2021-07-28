from domain.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListQuery import \
    GetDataOperationJobExecutionLogListQuery
from domain.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListRequest import \
    GetDataOperationJobExecutionLogListRequest
from domain.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListResponse import \
    GetDataOperationJobExecutionLogListResponse
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher

from injector import inject
from infrastructure.api.ResourceBase import ResourceBase


@controller()
class OperationJobExecutionLogResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self,
            req: GetDataOperationJobExecutionLogListRequest) -> GetDataOperationJobExecutionLogListResponse:
        """
        Get All Data Operation Jobs
        """
        query = GetDataOperationJobExecutionLogListQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result
