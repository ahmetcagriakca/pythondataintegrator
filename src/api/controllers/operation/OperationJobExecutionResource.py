from domain.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListQuery import \
    GetDataOperationJobExecutionListQuery
from domain.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListRequest import GetDataOperationJobExecutionListRequest
from domain.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListResponse import GetDataOperationJobExecutionListResponse
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher

from injector import inject
from infrastructure.api.ResourceBase import ResourceBase


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

