from injector import inject
from infrastructure.api.ResourceBase import ResourceBase
from domain.operation.CreateDataOperation.CreateDataOperationCommand import CreateDataOperationCommand
from domain.operation.CreateDataOperation.CreateDataOperationRequest import CreateDataOperationRequest
from domain.operation.DeleteDataOperation.DeleteDataOperationCommand import DeleteDataOperationCommand
from domain.operation.GetDataOperationList.GetDataOperationListQuery import GetDataOperationListQuery
from domain.operation.GetDataOperationList.GetDataOperationListRequest import GetDataOperationListRequest
from domain.operation.GetDataOperationList.GetDataOperationListResponse import GetDataOperationListResponse
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher


@controller()
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
        return "Data operation created"

    def delete(self, Id: int):
        """
        Delete Existing Data Operation
        """
        command = DeleteDataOperationCommand(Id=Id)
        self.dispatcher.dispatch(command)
        return "Data operation removed"
