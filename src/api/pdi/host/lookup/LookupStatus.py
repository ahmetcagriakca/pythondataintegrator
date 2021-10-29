from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from pdi.application.common.LookupStatus.LookupStatusQuery import LookupStatusQuery
from pdi.application.common.LookupStatus.LookupStatusRequest import LookupStatusRequest
from pdi.application.common.LookupStatus.LookupStatusResponse import LookupStatusResponse


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
