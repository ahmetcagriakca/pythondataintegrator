from injector import inject
from domain.common.LookupStatus.LookupStatusQuery import LookupStatusQuery
from domain.common.LookupStatus.LookupStatusRequest import LookupStatusRequest
from domain.common.LookupStatus.LookupStatusResponse import LookupStatusResponse
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher


@controller()
class LookupStatus(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: LookupStatusRequest) -> LookupStatusResponse:
        """
        Get All Connections
        """
        query = LookupStatusQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result
