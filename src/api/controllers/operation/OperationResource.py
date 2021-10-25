from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from domain.operation.DeleteDataOperation.DeleteDataOperationRequest import DeleteDataOperationRequest
from domain.operation.GetDataOperation.GetDataOperationQuery import GetDataOperationQuery
from domain.operation.GetDataOperation.GetDataOperationRequest import GetDataOperationRequest
from domain.operation.GetDataOperation.GetDataOperationResponse import GetDataOperationResponse
from domain.operation.CreateDataOperation.CreateDataOperationCommand import CreateDataOperationCommand
from domain.operation.CreateDataOperation.CreateDataOperationRequest import CreateDataOperationRequest
from domain.operation.DeleteDataOperation.DeleteDataOperationCommand import DeleteDataOperationCommand
from domain.operation.GetDataOperationList.GetDataOperationListQuery import GetDataOperationListQuery
from domain.operation.GetDataOperationList.GetDataOperationListRequest import GetDataOperationListRequest
from domain.operation.GetDataOperationList.GetDataOperationListResponse import GetDataOperationListResponse


class OperationByIdResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: GetDataOperationRequest) -> GetDataOperationResponse:
        """
        Get Data Operation By Id
        """
        query = GetDataOperationQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result


class OperationResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: GetDataOperationListRequest) -> GetDataOperationListResponse:
        """
        Get All Data Operations
        """
        query = GetDataOperationListQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result

    def post(self, req: CreateDataOperationRequest):
        """
        Data Operation definition
        """
        command = CreateDataOperationCommand(request=req)
        self.dispatcher.dispatch(command)

    def delete(self, req: DeleteDataOperationRequest):
        """
        Delete Existing Data Operation
        """
        command = DeleteDataOperationCommand(request=req)
        self.dispatcher.dispatch(command)
