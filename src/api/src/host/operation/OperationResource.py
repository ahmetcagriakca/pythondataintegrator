from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from src.application.operation.CreateDataOperation.CreateDataOperationCommand import CreateDataOperationCommand
from src.application.operation.CreateDataOperation.CreateDataOperationRequest import CreateDataOperationRequest
from src.application.operation.DeleteDataOperation.DeleteDataOperationCommand import DeleteDataOperationCommand
from src.application.operation.DeleteDataOperation.DeleteDataOperationRequest import DeleteDataOperationRequest
from src.application.operation.GetDataOperation.GetDataOperationQuery import GetDataOperationQuery
from src.application.operation.GetDataOperation.GetDataOperationRequest import GetDataOperationRequest
from src.application.operation.GetDataOperation.GetDataOperationResponse import GetDataOperationResponse
from src.application.operation.GetDataOperationList.GetDataOperationListQuery import GetDataOperationListQuery
from src.application.operation.GetDataOperationList.GetDataOperationListRequest import GetDataOperationListRequest
from src.application.operation.GetDataOperationList.GetDataOperationListResponse import GetDataOperationListResponse


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
