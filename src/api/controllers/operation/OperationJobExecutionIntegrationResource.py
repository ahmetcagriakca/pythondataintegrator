from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from domain.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListQuery import \
    GetDataOperationJobExecutionIntegrationListQuery
from domain.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListRequest import \
    GetDataOperationJobExecutionIntegrationListRequest
from domain.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListResponse import \
    GetDataOperationJobExecutionIntegrationListResponse


class OperationJobExecutionIntegrationResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self,
            req: GetDataOperationJobExecutionIntegrationListRequest) -> GetDataOperationJobExecutionIntegrationListResponse:
        """
        Get All Data Operation Jobs
        """
        query = GetDataOperationJobExecutionIntegrationListQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result
