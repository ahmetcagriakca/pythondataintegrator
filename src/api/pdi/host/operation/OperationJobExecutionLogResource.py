from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from pdi.application.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListQuery import \
    GetDataOperationJobExecutionLogListQuery
from pdi.application.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListRequest import \
    GetDataOperationJobExecutionLogListRequest
from pdi.application.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListResponse import \
    GetDataOperationJobExecutionLogListResponse


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
